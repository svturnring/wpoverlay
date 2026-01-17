#!/usr/bin/env bash
# Toggle wallpaper dimming overlay using GTK4 + Wayland Layer Shell.
# This script manages the Python overlay process (start/stop/theme switching).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="/tmp/wpoverlay.pid"

# Determine Python script path (installed or from source)
if [ -f "/usr/share/wpoverlay/wpoverlay-daemon.py" ]; then
    PYTHON_SCRIPT="/usr/share/wpoverlay/wpoverlay-daemon.py"
else
    PYTHON_SCRIPT="$SCRIPT_DIR/wpoverlay-daemon.py"
fi

# Parse command
COMMAND="${1:-toggle}"
THEME_NAME="${2:-}"

# Function to stop overlay
stop_overlay() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill -TERM "$PID" 2>/dev/null
            rm -f "$PID_FILE"
            echo "wpoverlay disabled"
            return 0
        else
            # PID file exists but process is dead, clean up
            rm -f "$PID_FILE"
        fi
    fi
    return 1
}

# Function to start overlay
start_overlay() {
    # Set LD_PRELOAD for gtk4-layer-shell
    export LD_PRELOAD="/usr/lib/libgtk4-layer-shell.so.0${LD_PRELOAD:+:$LD_PRELOAD}"

    # Launch Python overlay in background
    if [ -n "$THEME_NAME" ]; then
        python3 "$PYTHON_SCRIPT" "$THEME_NAME" > /dev/null 2>&1 &
    else
        python3 "$PYTHON_SCRIPT" > /dev/null 2>&1 &
    fi

    OVERLAY_PID=$!

    # Save PID
    echo "$OVERLAY_PID" > "$PID_FILE"

    if [ -n "$THEME_NAME" ]; then
        echo "wpoverlay enabled with theme: $THEME_NAME (PID: $OVERLAY_PID)"
    else
        echo "wpoverlay enabled (PID: $OVERLAY_PID)"
    fi
}

# Handle commands
case "$COMMAND" in
    toggle)
        if stop_overlay; then
            exit 0
        else
            start_overlay
        fi
        ;;

    theme)
        if [ -z "$THEME_NAME" ]; then
            echo "Error: theme name required"
            echo "Usage: wpoverlay theme <theme_name>"
            exit 1
        fi

        # Stop current overlay if running
        stop_overlay

        # Start with new theme
        start_overlay
        ;;

    stop)
        if stop_overlay; then
            exit 0
        else
            echo "wpoverlay is not running"
            exit 1
        fi
        ;;

    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "wpoverlay is already running (PID: $PID)"
                exit 1
            fi
        fi
        start_overlay
        ;;

    *)
        echo "Usage: wpoverlay [toggle|start|stop|theme <name>]"
        echo ""
        echo "Commands:"
        echo "  toggle          Toggle overlay on/off (default)"
        echo "  start           Start overlay"
        echo "  stop            Stop overlay"
        echo "  theme <name>    Switch to theme <name>.css"
        echo ""
        echo "Examples:"
        echo "  wpoverlay              # Toggle on/off"
        echo "  wpoverlay theme main   # Use main.css theme"
        echo "  wpoverlay theme custom # Use custom.css theme"
        exit 1
        ;;
esac
