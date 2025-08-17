#!/usr/bin/env python3
'''
User Management Script for Scraper App
Use this script to manage user licenses from your local machine
'''

import requests
import json
import base64
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

class UserManager:
    def __init__(self, github_token, repo_owner, repo_name):
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Load encryption key (same as used by the app)
        with open('security.key', 'rb') as f:
            self.cipher = Fernet(f.read())
    
    def list_users(self):
        '''List all registered users'''
        response = requests.get(f"{self.base_url}/users", headers=self.headers)
        if response.status_code == 200:
            users = response.json()
            print(f"Found {len(users)} registered users:")
            for user_file in users:
                machine_id = user_file['name'].replace('.dat', '')
                print(f"  - Machine ID: {machine_id}")
        else:
            print(f"Error listing users: {response.text}")
    
    def extend_license(self, machine_id, days):
        '''Extend license for a specific machine'''
        # Get current user data
        response = requests.get(f"{self.base_url}/users/{machine_id}.dat", headers=self.headers)
        if response.status_code != 200:
            print(f"User {machine_id} not found")
            return
        
        # Decrypt and update
        file_data = response.json()
        encrypted_content = base64.b64decode(file_data['content']).decode()
        user_data = json.loads(self.cipher.decrypt(encrypted_content.encode()).decode())
        
        # Extend license
        current_expiry = datetime.fromisoformat(user_data['license_expires'])
        new_expiry = current_expiry + timedelta(days=days)
        user_data['license_expires'] = new_expiry.isoformat()
        
        # Upload updated data
        encrypted_data = self.cipher.encrypt(json.dumps(user_data).encode()).decode()
        update_data = {
            'message': f'Extend license for {machine_id} by {days} days',
            'content': base64.b64encode(encrypted_data.encode()).decode(),
            'sha': file_data['sha']
        }
        
        response = requests.put(f"{self.base_url}/users/{machine_id}.dat", headers=self.headers, json=update_data)
        if response.status_code == 200:
            print(f"✅ Extended license for {machine_id} by {days} days (expires: {new_expiry.strftime('%Y-%m-%d')})")
        else:
            print(f"❌ Failed to extend license: {response.text}")

if __name__ == "__main__":
    # Configure your details here
    GITHUB_TOKEN = "your_token_here"
    REPO_OWNER = "your_username"
    REPO_NAME = "scraper-control"
    
    manager = UserManager(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
    
    print("Scraper App User Management")
    print("=" * 30)
    manager.list_users()
