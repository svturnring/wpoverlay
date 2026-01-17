# wpoverlay

Configurable Wayland wallpaper overlay with CSS theme support.

## Description

`wpoverlay` creates a customizable layer between your wallpaper and application windows on Wayland compositors using GTK4 and gtk4-layer-shell. Perfect for dimming bright wallpapers, adding color overlays, or applying another style options.

## Features

- CSS-based theme system
- Multiple theme support with easy switching
- Automatic theme persistence
- Simple toggle on/off
- Zero configuration required

## Dependencies

### Required
- Python 3
- python-gobject
- GTK4
- gtk4-layer-shell

### Compatible Compositors
- **Works with:** Hyprland, Sway, River, Wayfire, and other wlroots-based compositors that support layer-shell protocol
- **Does NOT work with:** GNOME Wayland (uses mutter, which has limited layer-shell support), KDE Plasma Wayland (KWin doesn't fully support gtk4-layer-shell)

**Why it doesn't work on GNOME/KDE:**
- GNOME's mutter compositor has incomplete wlr-layer-shell protocol implementation
- KDE's KWin doesn't support GTK4 layer-shell surfaces properly
- Both prioritize their own compositor-specific APIs over wlr-layer-shell

**Why it works on wlroots compositors:**
- Native wlr-layer-shell protocol support
- Designed for Wayland protocol compliance
- Proper layer stacking implementation

## Installation

### From AUR (Recommended)
```bash
yay -S wpoverlay
# or
paru -S wpoverlay
```

### Manual Installation
```bash
# Clone/download the repository
cd wpoverlay

# Build and install
makepkg -si
```

## Usage

### Basic Commands
```bash
wpoverlay              # Toggle on/off
wpoverlay start        # Start overlay
wpoverlay stop         # Stop overlay
wpoverlay theme main   # Switch to main theme
wpoverlay theme custom # Switch to custom theme
```

### First Run
On first run, wpoverlay automatically creates:
```
~/.config/wpoverlay/themes/main.css  # Default theme
~/.cache/wpoverlay/last_theme        # Last used theme tracker
```

### Theme System

Themes are CSS files located in `~/.config/wpoverlay/themes/`

**Default theme (main.css):**
```css
window {
    background: black;
    opacity: 0.5;
}
```

### Creating Custom Themes

Create a new CSS file in `~/.config/wpoverlay/themes/`:

```bash
# Example: dark theme
# ~/.config/wpoverlay/themes/dark.css
window {
    background: black;
    opacity: 0.8;
}

# Apply it
wpoverlay theme dark
```

### Theme Examples

**Light dimming (20%):**
```css
window {
    background: black;
    opacity: 0.2;
}
```

**Red tint:**
```css
window {
    background: rgba(150, 50, 50, 0.4);
}
```

**Blue cold tone:**
```css
window {
    background: rgba(30, 60, 120, 0.5);
}
```

**Gradient (dark top, light bottom):**
```css
window {
    background: linear-gradient(to bottom, 
        rgba(0, 0, 0, 0.8), 
        rgba(0, 0, 0, 0.2));
}
```

**Vignette (dark edges):**
```css
window {
    background: radial-gradient(ellipse at center, 
        transparent 0%, 
        rgba(0, 0, 0, 0.7) 100%);
}
```

## Compositor Integration

### Hyprland
```conf
# ~/.config/hypr/hyprland.conf

# Keybind to toggle
bind = $mainMod, D, exec, wpoverlay

# Auto-start on login
exec-once = wpoverlay
```

### Sway
```conf
# ~/.config/sway/config

# Keybind to toggle
bindsym $mod+d exec wpoverlay

# Auto-start on login
exec wpoverlay
```

### River
```bash
# ~/.config/river/init

# Keybind to toggle
riverctl map normal Super D spawn wpoverlay

# Auto-start
wpoverlay &
```

## Advanced Usage

### Multiple Theme Profiles

Create themed presets for different times of day:

```bash
# Day theme (light)
# ~/.config/wpoverlay/themes/day.css
window {
    background: black;
    opacity: 0.2;
}

# Evening theme (warm)
# ~/.config/wpoverlay/themes/evening.css
window {
    background: rgba(180, 100, 30, 0.4);
}

# Night theme (dark)
# ~/.config/wpoverlay/themes/night.css
window {
    background: black;
    opacity: 0.7;
}


# Switch themes
wpoverlay theme day
wpoverlay theme evening
wpoverlay theme night
```

### Theme Persistence

The last used theme is automatically saved to `~/.cache/wpoverlay/last_theme` and will be used on next start.

### Listing Themes
```bash
ls ~/.config/wpoverlay/themes/
```

## Troubleshooting

### Overlay doesn't appear
1. Check if gtk4-layer-shell is installed:
   ```bash
   pacman -Q gtk4-layer-shell
   ```

2. Verify your compositor supports layer-shell:
   ```bash
   # Run directly to see errors
   python3 /usr/share/wpoverlay/wpoverlay-daemon.py
   ```

3. Check if process is running:
   ```bash
   cat /tmp/wpoverlay.pid
   ps aux | grep wpoverlay-daemon
   ```

### Theme not applying
1. Verify theme file exists:
   ```bash
   ls ~/.config/wpoverlay/themes/
   ```

2. Check CSS syntax in your theme file

3. Restart overlay:
   ```bash
   wpoverlay stop
   wpoverlay start
   ```

### GNOME/KDE compatibility
Not supported due to compositor limitations. Use on wlroots-based compositors (Hyprland, Sway, etc.).

## Files and Directories

### Installed files
```
/usr/bin/wpoverlay                          # Main executable
/usr/share/wpoverlay/wpoverlay-daemon.py    # Python backend
/usr/share/doc/wpoverlay/README.md          # Documentation
```

### User files (auto-created)
```
~/.config/wpoverlay/themes/main.css   # Default theme
~/.cache/wpoverlay/last_theme         # Last used theme
/tmp/wpoverlay.pid                    # Process ID file
```

## License

MIT

## Author

svturnring <svturnring@icloud.com>
