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

class TMTunnelsAutoComplete:
    def __init__(self):
        self.register_url = "https://tmtunnels.id/execsignup.php"
        self.create_url = "https://tmtunnels.id/send.php"
        self.result_url = "https://tmtunnels.id/hasil.php"
        
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
            vmess_tls_match = re.search(r'vmess://([A-Za-z0-9+/=]+)', html_content)
            if vmess_tls_match:
                config_data['vmess_tls'] = f"vmess://{vmess_tls_match.group(1)}"
            
            # Look for multiple vmess links
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
        servers = [
            'do-4.tmtunnels.tech',
            'do-5.tmtunnels.tech', 
            'sg-1.tmtunnels.tech',
            'sg-2.tmtunnels.tech'
        ]
        
        answer = random.choice(answers)
        protocol = random.choice(protocols)
        server = random.choice(servers)
        
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
            else:
                print(f"💥 Account {i} failed!")
            
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

if __name__ == "__main__":
    auto_complete = TMTunnelsAutoComplete()
    
    try:
        print("🎯 TMTunnels Auto Register, Create & Get Config")
        print("=" * 50)
        count = int(input("Berapa akun yang ingin dibuat? "))
        delay = int(input("Delay antar request (detik)? [default: 3] ") or "3")
        
        auto_complete.run(count, delay)
        
    except KeyboardInterrupt:
        print("\n⛔ Script dihentikan oleh user.")
    except ValueError:
        print("❌ Input harus berupa angka!")
    except Exception as e:
        print(f"❌ Error: {e}")
