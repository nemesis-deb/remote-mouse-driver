#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

SERVICE_NAME="remote-mouse.service"
SERVICE_DEST="/etc/systemd/system/$SERVICE_NAME"

echo "Starting uninstallation of Remote Mouse Driver..."

# 1. Stop and disable the systemd service
echo "Stopping the service..."
sudo systemctl stop $SERVICE_NAME || true  # Continue even if service is not running

echo "Disabling the service..."
sudo systemctl disable $SERVICE_NAME || true # Continue even if service is not enabled

# 2. Remove the systemd service file
echo "Removing the systemd service file..."
sudo rm -f "$SERVICE_DEST"

# Reload systemd to apply changes
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# 3. Uninstall the Python package
echo "Uninstalling the remote-mouse-driver package..."
pip uninstall -y remote-mouse-driver

echo "Uninstallation complete."