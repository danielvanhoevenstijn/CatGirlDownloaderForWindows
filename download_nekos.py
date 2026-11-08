import os
import requests

# Using NekosAPI v4 which supports native random limits
API_URL = "https://api.nekosapi.com/v4/images/random"
OUTPUT_DIR = "downloaded_nekos"


def download_images(limit):
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  params = {"limit": limit}

  headers = {
      "User-Agent": "NekosDownloader/1.0 (PythonScript)",
      "Accept": "application/json",
  }

  print(f"Fetching {limit} image(s) from NekosAPI...")
  try:
    response = requests.get(API_URL, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching from API: {e}")
    return

  # NekosAPI v4 returns a list or a dictionary containing results
  images = data if isinstance(data, list) else data.get("items", [])

  if not images:
    print("No images returned from the API.")
    return

  print(f"Found {len(images)} images. Starting download...")

  for index, img_data in enumerate(images, start=1):
    # Extract the direct image URL from the response structure
    image_url = img_data.get("image_url") or img_data.get("url")
    if not image_url:
      continue

    # Get file extension or default to .jpg
    ext = os.path.splitext(image_url)[1] or ".jpg"
    filename = f"image_{index}{ext}"
    file_path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(file_path):
      print(f"Skipped (Already exists): {filename}")
      continue

    print(f"Downloading [{index}/{len(images)}]: {image_url}")
    try:
      img_response = requests.get(image_url, stream=True)
      if img_response.status_code == 200:
        with open(file_path, "wb") as f:
          for chunk in img_response.iter_content(1024):
            f.write(chunk)
      else:
        print(f"Failed to download image (Status code: {img_response.status_code})")
    except requests.exceptions.RequestException as e:
      print(f"Network error: {e}")

  print(f"\nDownload complete! Check the '{OUTPUT_DIR}' folder.")


def main():
  try:
    user_input = input("How many images would you like to download? ")
    limit = int(user_input)
    if limit <= 0:
      print("Please enter a number greater than 0.")
      return
  except ValueError:
    print("Invalid input. Please enter a valid integer.")
    return

  download_images(limit)


if __name__ == "__main__":
  main()
