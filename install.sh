#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define variables
SERVICE_NAME="remote-mouse.service"
SERVICE_DEST="/etc/systemd/system/$SERVICE_NAME"
DRIVER_DIR=$(pwd)
VENV_DIR="$DRIVER_DIR/venv"

echo "Starting installation of Remote Mouse Driver..."

# 1. Install system dependencies
echo "Installing ydotool..."
sudo pacman -Syu --noconfirm ydotool

# 2. Create and activate a Python virtual environment
echo "Creating Python virtual environment..."
python -m venv "$VENV_DIR"

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# 3. Install the driver
echo "Installing the remote-mouse-driver package..."
pip install .

# 4. Set up the systemd service
echo "Setting up the systemd service..."
# Update the ExecStart path in the service file
sed -i "s|ExecStart=.*|ExecStart=$VENV_DIR/bin/remote-mouse-driver|" "$DRIVER_DIR/$SERVICE_NAME"

sudo cp "$DRIVER_DIR/$SERVICE_NAME" "$SERVICE_DEST"

# Set correct permissions for the service file
sudo chmod 644 "$SERVICE_DEST"

# Reload systemd to recognize the new service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling the service to start on boot..."
sudo systemctl enable $SERVICE_NAME

# Start the service immediately
echo "Starting the service..."
sudo systemctl start $SERVICE_NAME

echo "Installation complete! The Remote Mouse Driver is now running."
echo "You can check its status with: sudo systemctl status $SERVICE_NAME"