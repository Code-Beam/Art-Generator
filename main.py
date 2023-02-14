import openai
import requests
from requests.structures import CaseInsensitiveDict
import os

openai.api_key = "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"

model_engine = "image-alpha-001"
url = "https://api.openai.com/v1/images/generations"

def save_image_from_url(image_url, filename, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, filename)

    with open(file_path, 'wb') as f:
        response = requests.get(image_url)
        f.write(response.content)

    return file_path

prompt = input("Enter prompt: ")
data = """
{
    """
data += f'"model": "{model_engine}",'
data += f'"prompt": "{prompt}",'
data += """
    "num_images":1,
    "size":"1024x1024",
    "response_format":"url"
}
"""

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["Authorization"] = f"Bearer {openai.api_key}"

resp = requests.post(url, headers=headers, data=data)

if resp.status_code != 200:
    raise ValueError("Failed to generate image")

response_text = resp.json()
image_url = response_text['data'][0]['url']

print(f"Image URL: {image_url}")

# write image URL to a file
with open("history.txt", "a") as f:
    f.write(f"{prompt} : {image_url}" + "\n")

prompt += ".png"
save_image_from_url(image_url,prompt,"images")