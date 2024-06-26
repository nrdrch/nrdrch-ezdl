import os
import subprocess
import toml
from rich.console import Console
from rich.spinner import Spinner

# Initialize rich console
console = Console()

# Define the path for settings.toml
settings_path = 'settings.toml'

# Check if settings.toml exists, if not create it with default values
def create_default_settings():
    console.print("Creating [bold yellow]settings.toml[/bold yellow] as it does not exist.")
    settings = {
        "paths": {
            "music_vault_path": r"$HOME\Music\ez-dl-Music",
            "video_vault_path": r"$HOME\Videos\ez-dl-Videos"
        },
        "settings": {
            "audio_quality": "0",
            "audio_format": "wav",
            "video_format": "mp4"
        },
        "aliases": {
            "audio_download_alias": "audio",
            "video_download_alias": "video"
        },
        "other": {
            "loading_animation": "aesthetic"
        
        }
    }
    with open(settings_path, 'w') as f:
        toml.dump(settings, f)

# Create settings.toml only if it does not exist
if not os.path.exists(settings_path):
    create_default_settings()

# Load settings from settings.toml
with open(settings_path, 'r') as f:
    settings = toml.load(f)
SPINNER = settings['other']['loading_animation']
AUDIO_ALIAS = settings['aliases']['audio_download_alias']
VIDEO_ALIAS = settings['aliases']['video_download_alias']
# Execute yt-dlp command based on user input
def execute_command(command, link, with_playlist):
    command = command.replace("{music_vault_path}", settings['paths']['music_vault_path'])
    command = command.replace("{video_vault_path}", settings['paths']['video_vault_path'])
    command = command.replace("{audio_quality}", settings['settings']['audio_quality'])
    command = command.replace("{audio_format}", settings['settings']['audio_format'])
    command = command.replace("{video_format}", settings['settings']['video_format'])
    command = command.replace("<youtube_link>", link)
    if with_playlist:
        command = command.replace("--no-playlist", "")
    
    with console.status("[bold cyan]Running Download command...[/bold cyan]", spinner=f"{SPINNER}", spinner_style="status.spinner", speed=1.0, refresh_per_second=12.5):
        try:
            result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
            if result.returncode == 0:
                console.print("[bold green]:white_check_mark:[/bold green] Download complete!")
            else:
                console.print(f"[bold red]:x: Failed![/bold red] {result.stderr}")
        except Exception as e:
            console.print(f"[bold red]:x: Exception![/bold red] {str(e)}")

# Main function to parse arguments and call the appropriate command
def main():
    import sys
    if len(sys.argv) < 2:
        console.print("[bold red]:x:[/bold red] No arguments provided. Use '--help' for usage information.")
        return
    
    if sys.argv[1] in ['--help', '-h']:
        console.print("[bold white]yt-dlp wrapper for simplicity[/bold white] \n"
                      "[bold cyan]Usage:[/bold cyan]\n"
                      " [#076841]ez-dl [/#076841]" f"{AUDIO_ALIAS}" " <[#DBC75D]link[/#DBC75D]> \n"
                      " [#076841]ez-dl [/#076841]" f"{VIDEO_ALIAS}" " <[#DBC75D]link[/#DBC75D]> \n"
                      "[#B1B1B1]optionally run with 'wp' or 'withplaylist', to download the whole playlist:[/#B1B1B1]\n"
                      " [#076841]ez-dl [/#076841]" f"{AUDIO_ALIAS}" " <[#DBC75D]link[/#DBC75D]> [#DBC75D]wp[/#DBC75D] \n"
                      " [#076841]ez-dl [/#076841]" f"{VIDEO_ALIAS}" " <[#DBC75D]link[/#DBC75D]> [#DBC75D]wp[/#DBC75D] \n")
        return

    if len(sys.argv) < 3:
        console.print("[bold red]:x:[/bold red] Invalid number of arguments. Use '--help' for usage information.")
        return
    
    alias = sys.argv[1]
    link = sys.argv[2]
    with_playlist = len(sys.argv) > 3 and (sys.argv[3] in ['wp', 'withplaylist'])

    if alias == settings['aliases']['audio_download_alias']:
        command = '$null = yt-dlp -x --audio-quality {audio_quality} --audio-format {audio_format} --ignore-errors --output "{music_vault_path}\\%(title)s.%(ext)s" --no-playlist "<youtube_link>"'
    elif alias == settings['aliases']['video_download_alias']:
        command = '$null = yt-dlp --ignore-errors --remux-video {video_format} --output "{video_vault_path}\\%(title)s.%(ext)s" --no-playlist "<youtube_link>"'
    elif alias == "open":
        command = ''
    else:
        console.print("[bold red]:x:[/bold red] Unknown alias.")
        return
    
    execute_command(command, link, with_playlist)

if __name__ == "__main__":
    main()
