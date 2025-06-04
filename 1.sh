# Update sistem
sudo apt update && sudo apt upgrade -y

# Install Python dan tools
sudo apt install python3 python3-pip python3-venv -y

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Install dependencies
pip install requests

# Jalankan script
python reg.py
