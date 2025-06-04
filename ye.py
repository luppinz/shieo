#!/usr/bin/env python3
import requests
import random
import string
import time
import json
import uuid
import re
from datetime import datetime
from urllib.parse import urlencode
import threading

# Import khusus untuk bot mode (opsional)
try:
    import telegram
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
    from telegram import Update
    import asyncio
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

class TMTunnelsAutoComplete:
    def __init__(self, telegram_token=None, chat_id=None):
        self.register_url = "https://tmtunnels.id/execsignup.php"
        self.create_url = "https://tmtunnels.id/send.php"
        self.result_url = "https://tmtunnels.id/hasil.php"
        
        # Telegram configuration - hanya simpan token dan chat_id
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        
        self.register_headers = {
            'authority': 'tmtunnels.id',
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://tmtunnels.id',
            'referer': 'https://tmtunnels.id/signup',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Pixel C Build/OPM8.190605.005) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        self.create_headers = {
            'authority': 'tmtunnels.id',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://tmtunnels.id',
            'referer': 'https://tmtunnels.id/create?salah',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="89", "Google Chrome";v="89"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Pixel C Build/OPM8.190605.005) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36'
        }
        
        self.result_headers = {
            'authority': 'tmtunnels.id',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'referer': 'https://tmtunnels.id/create?salah',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="89", "Google Chrome";v="89"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Pixel C Build/OPM8.190605.005) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36'
        }
        
        self.session = requests.Session()
    
    def send_telegram_sync(self, message):
        """Kirim pesan menggunakan HTTP request langsung"""
        if self.telegram_token and self.chat_id:
            try:
                url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
                payload = {
                    'chat_id': self.chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, json=payload, timeout=10)
                
                if response.status_code == 200:
                    print("✅ Pesan Telegram berhasil dikirim!")
                else:
                    print(f"❌ Error HTTP: {response.status_code}")
                    print(f"Response: {response.text}")
                        
            except Exception as e:
                print(f"❌ Error mengirim pesan Telegram: {e}")
        else:
            print("⚠️ Telegram token atau chat_id tidak dikonfigurasi")
    
    def format_account_message(self, account_info, account_number):
        """Format account information for Telegram message"""
        if account_info.get('vmess_tls') or account_info.get('vmess_ntls'):
            message = f"""
🎉 <b>AKUN TMTUNNELS #{account_number} BERHASIL DIBUAT</b>

👤 <b>Username:</b> <code>{account_info.get('username', 'N/A')}</code>
🔐 <b>Password:</b> <code>{account_info.get('password', 'N/A')}</code>
📝 <b>Remark:</b> <code>{account_info.get('remark', 'N/A')}</code>
🌐 <b>Domain:</b> <code>{account_info.get('domain', 'N/A')}</code>
🔒 <b>Port TLS:</b> <code>{account_info.get('port_tls', '443')}</code>
🔓 <b>Port NTLS:</b> <code>{account_info.get('port_ntls', '80')}</code>
🆔 <b>UUID:</b> <code>{account_info.get('id', 'N/A')}</code>
📂 <b>Path:</b> <code>{account_info.get('path', '/minacantik')}</code>
👥 <b>Max Login:</b> <code>{account_info.get('max_login', '2 IP')}</code>

🔗 <b>VMESS Links:</b>
"""
            if account_info.get('vmess_tls'):
                message += f"\n🔒 <b>TLS:</b>\n<code>{account_info['vmess_tls']}</code>\n"
            
            if account_info.get('vmess_ntls'):
                message += f"\n🔓 <b>NTLS:</b>\n<code>{account_info['vmess_ntls']}</code>\n"
            
            message += f"\n⏰ <b>Dibuat:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            message = f"""
❌ <b>AKUN TMTUNNELS #{account_number} GAGAL DIBUAT</b>

👤 <b>Username:</b> <code>{account_info.get('username', 'N/A')}</code>
🔐 <b>Password:</b> <code>{account_info.get('password', 'N/A')}</code>
📝 <b>Error:</b> <code>{account_info.get('error', 'Unknown error')}</code>
⏰ <b>Waktu:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return message
    
    def generate_username(self):
        """Generate random username"""
        prefix = "user"
        suffix = ''.join(random.choices(string.digits, k=6))
        return f"{prefix}{suffix}"
    
    def generate_email(self):
        """Generate random email"""
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    def generate_password(self):
        """Generate random password"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=12))
    
    def generate_remark(self):
        """Generate random remark"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    def generate_uuid(self):
        """Generate random UUID"""
        return str(uuid.uuid4())
    
    def parse_config_response(self, html_content):
        """Parse HTML response to extract configuration data"""
        config_data = {}
        
        try:
            # Extract Remark
            remark_match = re.search(r'Remark:\s*([^\n\r<]+)', html_content)
            if remark_match:
                config_data['remark'] = remark_match.group(1).strip()
            
            # Extract Domain
            domain_match = re.search(r'Domain:\s*([^\n\r<]+)', html_content)
            if domain_match:
                config_data['domain'] = domain_match.group(1).strip()
            
            # Extract Port TLS
            port_tls_match = re.search(r'Port TLS:\s*([^\n\r<]+)', html_content)
            if port_tls_match:
                config_data['port_tls'] = port_tls_match.group(1).strip()
            
            # Extract Port NTLS
            port_ntls_match = re.search(r'Port NTLS:\s*([^\n\r<]+)', html_content)
            if port_ntls_match:
                config_data['port_ntls'] = port_ntls_match.group(1).strip()
            
            # Extract ID/UUID
            id_match = re.search(r'Id:\s*([^\n\r<]+)', html_content)
            if id_match:
                config_data['id'] = id_match.group(1).strip()
            
            # Extract Path
            path_match = re.search(r'Path:\s*([^\n\r<]+)', html_content)
            if path_match:
                config_data['path'] = path_match.group(1).strip()
            
            # Extract Max Login
            max_login_match = re.search(r'Max Login:\s*([^\n\r<]+)', html_content)
            if max_login_match:
                config_data['max_login'] = max_login_match.group(1).strip()
            
            # Extract vmess links
            vmess_links = re.findall(r'vmess://([A-Za-z0-9+/=]+)', html_content)
            if len(vmess_links) >= 2:
                config_data['vmess_tls'] = f"vmess://{vmess_links[0]}"
                config_data['vmess_ntls'] = f"vmess://{vmess_links[1]}"
            elif len(vmess_links) == 1:
                config_data['vmess_tls'] = f"vmess://{vmess_links[0]}"
                
        except Exception as e:
            print(f"⚠️  Error parsing config: {e}")
            
        return config_data
    
    def register_account(self):
        """Register single account"""
        username = self.generate_username()
        email = self.generate_email()
        password = self.generate_password()
        
        data = {
            'username': username,
            'password': password,
            'email': email,
            'password1': password
        }
        
        print(f"🔄 Step 1: Registering account...")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print("-" * 60)
        
        try:
            response = self.session.post(self.register_url, headers=self.register_headers, data=data)
            print(f"   Registration Status: {response.status_code}")
            print(f"   Registration Response: {response.text}")
            
            # Check if registration successful
            if response.status_code == 200 and ("success" in response.text.lower() or "berhasil" in response.text.lower()):
                print("✅ Registration successful! Proceeding to create account...")
                return self.create_account(username, password)
            else:
                print("❌ Registration failed!")
                return False, {"username": username, "email": email, "password": password, "registration_response": response.text}
                
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False, {"username": username, "email": email, "password": password, "error": str(e)}
    
    def create_account(self, username, password):
        """Create account after successful registration"""
        remark = self.generate_remark()
        account_uuid = self.generate_uuid()
        
        # Possible answers and protocols
        answers = ['a', 'b', 'c', 'd']
        protocols = ['vmess', 'vless', 'trojan']
        # Server diubah menjadi hanya do-4.tmtunnels.tech
        server = 'do-4.tmtunnels.tech'
        
        answer = random.choice(answers)
        protocol = random.choice(protocols)
        
        create_data = {
            'answer': answer,
            'username': username,
            'remark': remark,
            'protocol': protocol,
            'answerTrue': answer,
            'idsoal': str(random.randint(1, 10)),
            'serv': server
        }
        
        print(f"🔄 Step 2: Creating account configuration...")
        print(f"   Username: {username}")
        print(f"   Remark: {remark}")
        print(f"   Protocol: {protocol}")
        print(f"   Server: {server}")
        print(f"   UUID: {account_uuid}")
        print(f"   Answer: {answer}")
        
        try:
            time.sleep(2)  # Wait before creating account
            response = self.session.post(self.create_url, headers=self.create_headers, data=create_data)
            print(f"   Creation Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Account creation successful! Getting configuration...")
                return self.get_account_config(username, password, remark, account_uuid, protocol, server)
            else:
                print("❌ Account creation failed!")
                return False, {
                    "username": username,
                    "password": password,
                    "remark": remark,
                    "uuid": account_uuid,
                    "protocol": protocol,
                    "server": server,
                    "creation_response": response.text
                }
                
        except Exception as e:
            print(f"❌ Creation error: {e}")
            return False, {
                "username": username,
                "password": password,
                "remark": remark,
                "uuid": account_uuid,
                "protocol": protocol,
                "server": server,
                "error": str(e)
            }
    
    def get_account_config(self, username, password, remark, account_uuid, protocol, server):
        """Get account configuration after creation"""
        params = {
            'remark': remark,
            'uuid': account_uuid,
            'protocol': protocol,
            'serv': server
        }
        
        result_url_with_params = f"{self.result_url}?{urlencode(params)}"
        
        print(f"🔄 Step 3: Getting account configuration...")
        print(f"   URL: {result_url_with_params}")
        
        try:
            time.sleep(3)  # Wait before getting config
            response = self.session.get(result_url_with_params, headers=self.result_headers)
            print(f"   Config Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Configuration retrieved successfully!")
                
                # Parse configuration from HTML
                config_data = self.parse_config_response(response.text)
                
                # Display configuration
                print("\n" + "="*60)
                print("🎉 ACCOUNT CONFIGURATION")
                print("="*60)
                print(f"Username: {username}")
                print(f"Password: {password}")
                print(f"Remark: {config_data.get('remark', remark)}")
                print(f"Domain: {config_data.get('domain', server)}")
                print(f"Port TLS: {config_data.get('port_tls', '443')}")
                print(f"Port NTLS: {config_data.get('port_ntls', '80')}")
                print(f"Id: {config_data.get('id', account_uuid)}")
                print(f"Path: {config_data.get('path', '/minacantik')}")
                print(f"Max Login: {config_data.get('max_login', '2 IP')}")
                
                if 'vmess_tls' in config_data:
                    print(f"vmess TLS: {config_data['vmess_tls']}")
                if 'vmess_ntls' in config_data:
                    print(f"vmess NTLS: {config_data['vmess_ntls']}")
                
                print("="*60)
                
                # Complete account info
                complete_info = {
                    "username": username,
                    "password": password,
                    "remark": config_data.get('remark', remark),
                    "domain": config_data.get('domain', server),
                    "port_tls": config_data.get('port_tls', '443'),
                    "port_ntls": config_data.get('port_ntls', '80'),
                    "id": config_data.get('id', account_uuid),
                    "path": config_data.get('path', '/minacantik'),
                    "max_login": config_data.get('max_login', '2 IP'),
                    "vmess_tls": config_data.get('vmess_tls', ''),
                    "vmess_ntls": config_data.get('vmess_ntls', '')
                }
                
                return True, complete_info
            else:
                print("❌ Failed to retrieve configuration!")
                return False, {"username": username, "password": password, "error": response.text}
                
        except Exception as e:
            print(f"❌ Error getting configuration: {e}")
            return False, {"username": username, "password": password, "error": str(e)}
    
    def run(self, count=1, delay=3):
        """Run auto registration, creation, and configuration retrieval"""
        print("🚀 TMTunnels Auto Register, Create & Get Config Script")
        print("=" * 60)
        
        success_count = 0
        results = []
        
        # Send start notification to Telegram
        start_message = f"""
🚀 <b>TMTUNNELS AUTO SCRIPT DIMULAI</b>

📊 <b>Target:</b> {count} akun
🌐 <b>Server:</b> do-4.tmtunnels.tech
⏱️ <b>Delay:</b> {delay} detik
🕐 <b>Dimulai:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        self.send_telegram_sync(start_message)
        
        for i in range(1, count + 1):
            print(f"\n📝 Processing account {i} of {count}...")
            print("=" * 60)
            
            success, account_info = self.register_account()
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'account_number': i,
                'success': success,
                **account_info
            }
            
            results.append(log_entry)
            
            if success:
                success_count += 1
                print(f"🎉 Account {i} completed successfully!")
                
                # Send success notification to Telegram
                telegram_message = self.format_account_message(account_info, i)
                self.send_telegram_sync(telegram_message)
            else:
                print(f"💥 Account {i} failed!")
                
                # Send failure notification to Telegram
                telegram_message = self.format_account_message(account_info, i)
                self.send_telegram_sync(telegram_message)
            
            # Save to log file
            with open('tmtunnels_log.json', 'a') as f:
                f.write(json.dumps(log_entry, indent=2) + '\n')
            
            print("=" * 60)
            
            if i < count:  # Don't delay after last account
                print(f"⏳ Waiting {delay} seconds before next account...")
                time.sleep(delay)
        
        # Summary
        print(f"\n📊 SUMMARY:")
        print(f"   Total accounts processed: {count}")
        print(f"   Successful: {success_count}")
        print(f"   Failed: {count - success_count}")
        print(f"   Success rate: {(success_count/count)*100:.1f}%")
        print(f"\n📁 Check file 'tmtunnels_log.json' for detailed logs.")
        
        # Send summary to Telegram
        summary_message = f"""
📊 <b>TMTUNNELS AUTO SCRIPT SELESAI</b>

✅ <b>Berhasil:</b> {success_count}/{count}
❌ <b>Gagal:</b> {count - success_count}/{count}
📈 <b>Success Rate:</b> {(success_count/count)*100:.1f}%
🌐 <b>Server:</b> do-4.tmtunnels.tech
🕐 <b>Selesai:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📁 Log tersimpan di: tmtunnels_log.json
"""
        self.send_telegram_sync(summary_message)
        
        # Save summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_processed': count,
            'successful': success_count,
            'failed': count - success_count,
            'success_rate': f"{(success_count/count)*100:.1f}%",
            'results': results
        }
        
        with open('tmtunnels_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)

# Telegram Bot Handler Class (hanya jika library tersedia)
class TMTunnelsTelegramBot:
    def __init__(self, telegram_token):
        if not TELEGRAM_AVAILABLE:
            raise ImportError("python-telegram-bot tidak terinstall!")
            
        self.telegram_token = telegram_token
        self.app = ApplicationBuilder().token(telegram_token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup command handlers"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("create", self.create_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🎉 <b>Selamat datang di TMTunnels Auto Bot!</b>

🤖 Bot ini dapat membantu Anda membuat akun TMTunnels secara otomatis.
🌐 <b>Server:</b> do-4.tmtunnels.tech

📋 <b>Perintah yang tersedia:</b>
/start - Menampilkan pesan selamat datang
/help - Menampilkan bantuan
/create [jumlah] - Membuat akun TMTunnels

💡 <b>Contoh penggunaan:</b>
<code>/create 5</code> - Membuat 5 akun TMTunnels

⚠️ <b>Catatan:</b> Proses pembuatan akun membutuhkan waktu, harap bersabar.
"""
        await update.message.reply_text(welcome_message, parse_mode='HTML')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
📖 <b>BANTUAN TMTUNNELS AUTO BOT</b>

🔧 <b>Perintah yang tersedia:</b>

/start - Menampilkan pesan selamat datang
/help - Menampilkan bantuan ini
/create [jumlah] - Membuat akun TMTunnels

💡 <b>Cara menggunakan:</b>
1. Ketik <code>/create 1</code> untuk membuat 1 akun
2. Ketik <code>/create 5</code> untuk membuat 5 akun
3. Bot akan mengirim hasil ke chat ini

⚠️ <b>Batasan:</b>
- Maksimal 10 akun per request
- Delay 3 detik antar pembuatan akun
- Proses berjalan di background
- Server: do-4.tmtunnels.tech

🆘 <b>Butuh bantuan?</b>
Hubungi developer jika mengalami masalah.
"""
        await update.message.reply_text(help_message, parse_mode='HTML')
    
    async def create_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /create command"""
        try:
            # Get number of accounts to create
            if context.args:
                count = int(context.args[0])
                if count > 10:
                    await update.message.reply_text("❌ Maksimal 10 akun per request!")
                    return
                elif count < 1:
                    await update.message.reply_text("❌ Jumlah akun minimal 1!")
                    return
            else:
                count = 1
            
            chat_id = update.effective_chat.id
            
            # Send confirmation message
            confirm_message = f"""
🔄 <b>Memulai pembuatan {count} akun TMTunnels...</b>

🌐 <b>Server:</b> do-4.tmtunnels.tech
⏳ Proses sedang berjalan, harap tunggu...
📱 Hasil akan dikirim ke chat ini secara real-time.
"""
            await update.message.reply_text(confirm_message, parse_mode='HTML')
            
            # Run account creation in background thread
            def run_creation():
                # Gunakan requests untuk notifikasi, bukan async bot
                auto_complete = TMTunnelsAutoComplete(
                    telegram_token=self.telegram_token,
                    chat_id=chat_id
                )
                auto_complete.run(count=count, delay=3)
            
            # Start background thread
            thread = threading.Thread(target=run_creation)
            thread.daemon = True
            thread.start()
            
        except ValueError:
            await update.message.reply_text("❌ Format salah! Gunakan: /create [jumlah]\nContoh: /create 5")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        message = """
🤖 Saya adalah TMTunnels Auto Bot.

Gunakan perintah berikut:
/start - Memulai bot
/help - Bantuan
/create [jumlah] - Membuat akun

Contoh: <code>/create 3</code>
🌐 Server: do-4.tmtunnels.tech
"""
        await update.message.reply_text(message, parse_mode='HTML')
    
    def run_bot(self):
        """Run the Telegram bot"""
        try:
            print("🤖 Starting Telegram Bot...")
            self.app.run_polling()
        except KeyboardInterrupt:
            print("\n⛔ Bot dihentikan oleh user.")
        except Exception as e:
            print(f"❌ Bot error: {e}")
        finally:
            print("🔄 Bot cleanup completed.")

if __name__ == "__main__":
    print("🎯 TMTunnels Auto Register, Create & Get Config with Telegram Support")
    print("🌐 Server: do-4.tmtunnels.tech")
    print("=" * 70)
    
    mode = input("Pilih mode:\n1. Manual (tanpa bot)\n2. Telegram Bot\nPilihan (1/2): ").strip()
    
    if mode == "2":
        # Telegram Bot Mode
        if not TELEGRAM_AVAILABLE:
            print("❌ python-telegram-bot tidak terinstall!")
            print("Install dengan: pip install python-telegram-bot")
            exit(1)
            
        telegram_token = input("Masukkan Telegram Bot Token: ").strip()
        if not telegram_token:
            print("❌ Token Telegram diperlukan!")
            exit(1)
        
        try:
            bot = TMTunnelsTelegramBot(telegram_token)
            bot.run_bot()
        except KeyboardInterrupt:
            print("\n⛔ Bot dihentikan oleh user.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        # Manual Mode - tidak memerlukan async
        try:
            count = int(input("Berapa akun yang ingin dibuat? "))
            delay = int(input("Delay antar request (detik)? [default: 3] ") or "3")
            
            # Optional Telegram notification
            use_telegram = input("Gunakan notifikasi Telegram? (y/n): ").lower().strip()
            telegram_token = None
            chat_id = None
            
            if use_telegram == 'y':
                telegram_token = input("Masukkan Telegram Bot Token: ").strip()
                chat_id = input("Masukkan Chat ID: ").strip()
                
                if not telegram_token or not chat_id:
                    print("⚠️ Token atau Chat ID kosong, melanjutkan tanpa notifikasi Telegram")
                    telegram_token = None
                    chat_id = None
            
            auto_complete = TMTunnelsAutoComplete(telegram_token, chat_id)
            auto_complete.run(count, delay)
            
        except KeyboardInterrupt:
            print("\n⛔ Script dihentikan oleh user.")
        except ValueError:
            print("❌ Input harus berupa angka!")
        except Exception as e:
            print(f"❌ Error: {e}")
