import requests
import time

# API key, show ID, and passed parameters (which we use to set the number of episodes we are downloading)
api_key = "YOUR KEY HERE" # API key is in your account profile under API access
show_id = "YOUR SHOW ID HERE" # Show ID is the last thing in your address bar for a show ex. https://dashboard.transistor.fm/shows/show_id
params = {'pagination[per]': 1} # Adjust this number for how many episodes you want to download
timeout = 60
headers = {"x-api-key": api_key,"Content-Type": "application/json"}

# Get a list of episodes in a show, number of episodes is controlled by params
api_response = requests.get(f"https://api.transistor.fm/v1/episodes?show_id={show_id}", params=params, headers=headers)

# Checks if API call was successful
if api_response.status_code == 200:
    episodes = api_response.json()["data"]
    time.sleep(1)

    for episode in episodes:
        # the following are used to name the file and grab the audio url
        # you can use other attributes too, found here: https://developers.transistor.fm/#Episode
        ep_number = episode["attributes"]["number"]
        pub_date = episode["attributes"]["formatted_published_at"]
        title = episode['attributes']['title']
        title = title.replace("/", " ")
        audio_url = episode['attributes']['media_url']
        print(f"Downloading: EP.{ep_number} '{title}' ({pub_date}).mp3")

        # Download the audio file, wait to avoid rate limits
        try:
            audio_response = requests.get(audio_url, timeout=timeout)
            audio_response.raise_for_status()
            with open(f"EP.{ep_number} '{title}' ({pub_date}).mp3", "wb") as file:
                file.write(audio_response.content)
            time.sleep(1)
        except requests.exceptions.Timeout:
            print(f"Timeout occoured. Skipping {title}")
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"Error {e}. Skipping {title}")
            time.sleep(1)

# Gives error message if API call fails
else:
    print(f"API access failed: {api_response.status_code}")