INSTALL_DIR := /usr/local/bin
SCRIPT_DIR := /opt/steghide-mkv
VENV_DIR := $(SCRIPT_DIR)/venv
PYTHON := python3

.PHONY: all install uninstall deps venv check

all: install

check:
	@command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 is required but not installed."; exit 1; }
	@command -v pip3 >/dev/null 2>&1 || { echo "ERROR: pip3 is required but not installed."; exit 1; }

venv: check
	@echo "[*] Creating virtual environment at $(VENV_DIR)..."
	@sudo mkdir -p $(SCRIPT_DIR)
	@sudo $(PYTHON) -m venv $(VENV_DIR)

deps: venv
	@echo "[*] Installing steghide..."
	@if command -v apt-get >/dev/null 2>&1; then \
		echo "  -> Detected Debian/Ubuntu (apt)"; \
		sudo apt-get update -qq && sudo apt-get install -y steghide; \
	elif command -v dnf >/dev/null 2>&1; then \
		echo "  -> Detected Fedora/RHEL (dnf)"; \
		sudo dnf install -y steghide; \
	elif command -v yum >/dev/null 2>&1; then \
		echo "  -> Detected CentOS/RHEL (yum)"; \
		sudo yum install -y steghide; \
	elif command -v pacman >/dev/null 2>&1; then \
		echo "  -> Detected Arch Linux (pacman)"; \
		sudo pacman -Sy --noconfirm steghide; \
	elif command -v zypper >/dev/null 2>&1; then \
		echo "  -> Detected openSUSE (zypper)"; \
		sudo zypper install -y steghide; \
	elif command -v apk >/dev/null 2>&1; then \
		echo "  -> Detected Alpine Linux (apk)"; \
		sudo apk add --no-cache steghide; \
	elif command -v brew >/dev/null 2>&1; then \
		echo "  -> Detected macOS (brew)"; \
		brew install steghide; \
	else \
		echo "ERROR: Could not detect a supported package manager."; \
		echo "Please install steghide manually and re-run make."; \
		exit 1; \
	fi

	@echo "[*] Installing Python dependencies..."
	@sudo $(VENV_DIR)/bin/pip install --upgrade pip
	@sudo $(VENV_DIR)/bin/pip install \
		opencv-python \
		numpy

install: deps
	@echo "[*] Installing Python scripts to $(SCRIPT_DIR)..."
	@sudo cp steghide-mkv.py $(SCRIPT_DIR)/steghide-mkv.py
	@sudo cp steghide-extract-mkv.py $(SCRIPT_DIR)/steghide-extract-mkv.py
	@sudo chmod 644 $(SCRIPT_DIR)/steghide-mkv.py
	@sudo chmod 644 $(SCRIPT_DIR)/steghide-extract-mkv.py

	@echo "[*] Installing steghide-mkv command to $(INSTALL_DIR)..."
	@sudo cp steghide-mkv.sh $(INSTALL_DIR)/steghide-mkv
	@sudo chmod +x $(INSTALL_DIR)/steghide-mkv

	@echo "[✓] Installation complete. Run 'steghide-mkv' to get started."

uninstall:
	@echo "[*] Removing steghide-mkv..."
	@sudo rm -f $(INSTALL_DIR)/steghide-mkv
	@sudo rm -rf $(SCRIPT_DIR)
	@echo "[✓] Uninstall complete."