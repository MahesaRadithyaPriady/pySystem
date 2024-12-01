#!/bin/bash

echo "Installing Fake Error Application..."
sudo apt update
sudo apt install python3 python3-tk -y

echo "Installation Complete. Running Fake Error Application now..."
# Jalankan aplikasi secara otomatis
python3 main.py
