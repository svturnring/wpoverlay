#!/usr/bin/env python3
"""
Wallpaper dimming overlay using GTK4 + Wayland Layer Shell.
Creates a transparent layer on BOTTOM level (between wallpaper and windows).
"""

import os
import signal
import sys
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gtk4LayerShell", "1.0")
from gi.repository import GLib, Gtk, Gtk4LayerShell


class DimOverlay(Gtk.Window):
    def __init__(self, theme_file):
        super().__init__()

        # Initialize layer shell for this window
        Gtk4LayerShell.init_for_window(self)

        # Load and apply CSS theme
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_path(str(theme_file))
            print(f"Theme loaded: {theme_file.name}", flush=True)
        except Exception as e:
            print(f"Error loading theme: {e}", flush=True)
            # Fallback to default CSS
            css_provider.load_from_data(b"""
                window {
                    background: black;
                    opacity: 0.5;
                }
            """)

        Gtk.StyleContext.add_provider_for_display(
            self.get_display(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Set layer to BOTTOM (between wallpaper and windows)
        Gtk4LayerShell.set_layer(self, Gtk4LayerShell.Layer.BOTTOM)

        # Anchor to all edges to cover entire screen
        Gtk4LayerShell.set_anchor(self, Gtk4LayerShell.Edge.LEFT, True)
        Gtk4LayerShell.set_anchor(self, Gtk4LayerShell.Edge.RIGHT, True)
        Gtk4LayerShell.set_anchor(self, Gtk4LayerShell.Edge.TOP, True)
        Gtk4LayerShell.set_anchor(self, Gtk4LayerShell.Edge.BOTTOM, True)

        # Don't reserve exclusive space
        Gtk4LayerShell.set_exclusive_zone(self, -1)

        # Set namespace for layer identification
        Gtk4LayerShell.set_namespace(self, "wpoverlay")

        # Don't accept keyboard input
        Gtk4LayerShell.set_keyboard_mode(self, Gtk4LayerShell.KeyboardMode.NONE)

        # Create drawing area for the overlay
        drawing_area = Gtk.DrawingArea()
        drawing_area.set_size_request(1920, 1080)
        drawing_area.set_hexpand(True)
        drawing_area.set_vexpand(True)

        self.set_child(drawing_area)

        # Connect close request
        self.connect("close-request", self.on_close)

        print("Overlay created on BOTTOM layer", flush=True)

    def on_close(self, *args):
        """Handle window close."""
        return False


def get_config_dir():
    """Get configuration directory path."""
    xdg_config = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config:
        config_home = Path(xdg_config)
    else:
        config_home = Path.home() / '.config'

    return config_home / 'wpoverlay'


def get_cache_dir():
    """Get cache directory path."""
    xdg_cache = os.environ.get('XDG_CACHE_HOME')
    if xdg_cache:
        cache_home = Path(xdg_cache)
    else:
        cache_home = Path.home() / '.cache'

    cache_dir = cache_home / 'wpoverlay'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def ensure_default_theme(themes_dir):
    """Create default main.css theme if it doesn't exist."""
    main_theme = themes_dir / "main.css"
    if not main_theme.exists():
        default_css = """window {
    background: black;
    opacity: 0.5;
}
"""
        main_theme.write_text(default_css)
        print(f"Created default theme: {main_theme}", flush=True)


def get_last_theme():
    """Get the last used theme name from cache."""
    cache_dir = get_cache_dir()
    last_theme_file = cache_dir / "last_theme"

    if last_theme_file.exists():
        try:
            return last_theme_file.read_text().strip()
        except Exception:
            pass

    return "main"


def save_last_theme(theme_name):
    """Save the last used theme name to cache."""
    cache_dir = get_cache_dir()
    last_theme_file = cache_dir / "last_theme"
    last_theme_file.write_text(theme_name)


def main():
    # Suppress GTK warnings
    os.environ["G_MESSAGES_DEBUG"] = ""

    # Get theme name from command line arguments
    theme_name = sys.argv[1] if len(sys.argv) > 1 else None

    # Get configuration directory
    config_dir = get_config_dir()
    themes_dir = config_dir / "themes"
    themes_dir.mkdir(parents=True, exist_ok=True)

    # Ensure default theme exists
    ensure_default_theme(themes_dir)

    # Determine which theme to use
    if theme_name:
        theme_file = themes_dir / f"{theme_name}.css"
        if not theme_file.exists():
            print(f"Theme '{theme_name}' not found at {theme_file}", flush=True)
            sys.exit(1)
    else:
        # Use last theme or default to main
        theme_name = get_last_theme()
        theme_file = themes_dir / f"{theme_name}.css"
        if not theme_file.exists():
            theme_name = "main"
            theme_file = themes_dir / f"{theme_name}.css"

    # Save current theme as last used
    save_last_theme(theme_name)

    # Create main loop
    main_loop = GLib.MainLoop()

    # Set up signal handlers for clean shutdown
    def signal_handler(sig, frame):
        main_loop.quit()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Create and show overlay
    overlay = DimOverlay(theme_file)
    overlay.present()

    # Run GLib main loop
    try:
        main_loop.run()
    except KeyboardInterrupt:
        main_loop.quit()


if __name__ == "__main__":
    main()
