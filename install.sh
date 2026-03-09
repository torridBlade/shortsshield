#!/bin/bash
# ShortsShield Installation Script for Linux
# This script installs ShortsShield and all dependencies

set -e

VERSION="1.0.0"
REPO_URL="https://github.com/yourusername/shortsshield"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           ShortsShield v${VERSION} - Linux Installer            ║"
echo "║  YouTube Shorts Watcher with Ad Replacement Fun Facts        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Detect Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
fi

echo "✓ Detected OS: $OS"
echo ""

# Install system dependencies based on distro
echo "📦 Installing system dependencies..."

case $OS in
    ubuntu|debian)
        sudo apt-get update
        sudo apt-get install -y \
            python3 python3-pip python3-dev \
            libgtk-3-0 libgtk-3-dev \
            libwebkit2gtk-4.0-0 libwebkit2gtk-4.0-dev \
            gir1.2-gtk-3.0 gir1.2-webkit2-4.0 \
            fonts-fira-sans
        ;;
    fedora|rhel|centos)
        sudo dnf install -y \
            python3 python3-devel python3-pip \
            gtk3 gtk3-devel \
            webkit2gtk3 webkit2gtk3-devel \
            gobject-introspection-devel \
            fira-fonts
        ;;
    arch|manjaro)
        sudo pacman -Sy --noconfirm \
            python python-pip \
            gtk3 \
            webkit2gtk \
            gobject-introspection \
            ttf-fira-sans
        ;;
    opensuse*)
        sudo zypper install -y \
            python3 python3-devel python3-pip \
            gtk3-devel \
            webkit2gtk3-devel \
            typelib-1_0-Gtk-3_0 typelib-1_0-WebKit2-4_0 \
            fonts-fira-sans
        ;;
    *)
        echo "⚠️  Unsupported distribution: $OS"
        echo "Please install the following packages manually:"
        echo "  - Python 3.8+"
        echo "  - GTK 3"
        echo "  - WebKit2GTK"
        echo "  - GObject Introspection"
        exit 1
        ;;
esac

echo "✓ System dependencies installed"
echo ""

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install --user \
    requests \
    PyGObject

echo "✓ Python dependencies installed"
echo ""

# Create application directory
APP_DIR="${HOME}/.local/share/shortsshield"
BIN_DIR="${HOME}/.local/bin"

mkdir -p "$APP_DIR"
mkdir -p "$BIN_DIR"

echo "📁 Installing files..."

# Copy main application
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/shorts-facts.py" "$APP_DIR/shortsshield"
chmod +x "$APP_DIR/shortsshield"

# Create launcher script
cat > "$BIN_DIR/shortsshield" << 'EOF'
#!/bin/bash
exec python3 ~/.local/share/shortsshield/shortsshield "$@"
EOF
chmod +x "$BIN_DIR/shortsshield"

# Create desktop entry
mkdir -p "${HOME}/.local/share/applications"
cat > "${HOME}/.local/share/applications/shortsshield.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=ShortsShield
Comment=YouTube Shorts with Fun Facts replacing ads
Exec=shortsshield
Icon=media-playback-start
Categories=Multimedia;Video;
Terminal=false
Keywords=youtube;shorts;video;fun;facts;
EOF

echo "✓ Application files installed"
echo ""

# Update PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠️  Adding $BIN_DIR to PATH"
    if [ -f "$HOME/.bashrc" ]; then
        echo "export PATH=\$PATH:$BIN_DIR" >> "$HOME/.bashrc"
    fi
    if [ -f "$HOME/.zshrc" ]; then
        echo "export PATH=\$PATH:$BIN_DIR" >> "$HOME/.zshrc"
    fi
    export PATH=$PATH:$BIN_DIR
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              Installation Complete! 🎉                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "To launch ShortsShield:"
echo "  $ shortsshield"
echo ""
echo "Or find it in your application menu as 'ShortsShield'"
echo ""
echo "To uninstall:"
echo "  rm -rf ~/.local/share/shortsshield"
echo "  rm ~/.local/bin/shortsshield"
echo "  rm ~/.local/share/applications/shortsshield.desktop"
echo ""
echo "Enjoy learning fun facts while watching shorts! 📚"
