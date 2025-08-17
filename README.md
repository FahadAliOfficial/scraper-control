# Scraper App Control Repository

This private repository contains control files for the Scraper Application.

## Directory Structure

### `/control/`
- `version.json` - Version control and update management
- `kill_switch.json` - Remote disable functionality
- `app_settings.json` - Application configuration

### `/users/`
- Individual user license files (encrypted)
- Format: `{machine_id}.dat`

### `/logs/`
- Usage logs and analytics
- Error reports from users

## Usage

### To Release a New Version:
1. Update `control/version.json` with new version number
2. Upload new executable to GitHub Releases
3. Update `download_url` in version.json
4. Set `force_update: true` if mandatory

### To Disable the App:
1. Edit `control/kill_switch.json`
2. Set `global_kill: true` for all users
3. Or add specific machine IDs to `machine_kills` array

### To Extend User License:
1. Find user file in `/users/{machine_id}.dat`
2. Update the `license_expires` field
3. Commit changes

### To Track Users:
- Check `/users/` directory for all registered machines
- Each file contains encrypted user data including:
  - Registration date
  - License expiry
  - Usage statistics
  - Last seen date

## Security

- All user data is encrypted using Fernet encryption
- Machine IDs are generated from hardware signatures
- Licenses are tied to specific machines
- All API access requires GitHub token authentication

## Monitoring

The app automatically:
- Checks license status daily
- Reports usage statistics
- Checks for kill switch hourly
- Looks for updates on startup
