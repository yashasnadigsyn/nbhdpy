import yt_dlp as youtube_dl

def get_song_info(url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'simulate': True,
        'ignoreerrors': True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)

            if not info_dict:
                return None

            title = info_dict.get('title', 'N/A')
            duration_seconds = info_dict.get('duration', 0)
            view_count = info_dict.get('view_count', 0)

            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            duration_formatted = f"{minutes:02d}:{seconds:02d}"

            if view_count >= 1_000_000_000:
                views_formatted = f"{view_count / 1_000_000_000:.1f}B"
            elif view_count >= 1_000_000:
                views_formatted = f"{view_count / 1_000_000:.1f}M"
            elif view_count >= 1_000:
                views_formatted = f"{view_count / 1_000:.1f}K"
            else:
                views_formatted = str(view_count)

            return {
                'title': title,
                'duration': duration_formatted,
                'views': views_formatted,
            }

    except youtube_dl.utils.DownloadError as e:
        print(f"Error downloading information: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
