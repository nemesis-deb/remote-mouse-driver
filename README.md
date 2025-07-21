 Remote Mouse Driver

This project provides a simple driver to control your mouse using a serial device. The driver runs as a `systemd` service in the background, continuously listening for commands from the serial port.

## Features

- **Mouse Control**: Move the cursor up, down, left, and right.
- **Click Events**: Perform left and right clicks.
- **Speed Control**: Adjust the cursor speed on the fly.
- **Background Service**: Runs as a `systemd` service, starting automatically on boot.
- **Easy Installation**: A simple `install.sh` script handles everything.
- **Robust Connection**: Automatically retries to connect to the serial port if disconnected.

## Requirements

- **OS**: A Linux distribution with `systemd` (e.g., Arch Linux, Ubuntu, Debian).
- **Python**: Python 3.6+
- **Dependencies**:
  - `ydotool`: A command-line tool for programmatic input control.
  - `pyserial`: A Python library for serial port communication.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/remote-mouse-driver.git
    cd remote-mouse-driver
    ```

2.  **Make the installation script executable**:
    ```bash
    chmod +x install.sh
    ```

3.  **Run the installation script**:
    ```bash
    ./install.sh
    ```
    The script will:
    - Install `ydotool` and `python-pip` using `pacman`.
    - Install the required Python packages.
    - Install the driver as a Python package.
    - Copy the `systemd` service file to the correct location.
    - Reload the `systemd` daemon, enable, and start the service.

## Usage

Once installed, the driver will run automatically in the background. No manual intervention is needed.

### Managing the Service

You can manage the service using standard `systemctl` commands:

-   **Check the status**:
    ```bash
    sudo systemctl status remote-mouse.service
    ```
-   **Stop the service**:
    ```bash
    sudo systemctl stop remote-mouse.service
    ```
-   **Start the service**:
    ```bash
    sudo systemctl start remote-mouse.service
    ```
-   **Restart the service**:
    ```bash
    sudo systemctl restart remote-mouse.service
    ```
-   **View logs**:
    ```bash
    journalctl -u remote-mouse.service -f
    ```

## Uninstallation

To remove the driver and all related files, run the `uninstall.sh` script:

1.  **Make the uninstallation script executable**:
    ```bash
    chmod +x uninstall.sh
    ```
2.  **Run the script**:
    ```bash
    ./uninstall.sh
    ```
This will stop and disable the `systemd` service, remove the service file, and uninstall the Python package.