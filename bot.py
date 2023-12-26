from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import random
import requests
from x import tweet


# get quote from API
def getquote():
    url = "https://zenquotes.io/api/quotes"
    response = requests.get(url)
    quote = response.json()[0]["q"]
    author = response.json()[0]["a"]
    return quote, author


# select one of the random image from from folder for bakcground
def getrandimg():
    path = "img"
    # Get a list of all the image filenames in the folder
    image_filenames = [
        filename
        for filename in os.listdir(path)
        if filename.endswith(".jpg") or filename.endswith(".png")
    ]
    # Select a random image filename from the list
    random_image_filename = random.choice(image_filenames)
    ans = path + "/" + random_image_filename
    return ans


# used for splitting the text in diffrent lines so that it can be easily read on picture
def wraptext(txt, width):
    ans = []
    x = ""
    n = 0
    for char in txt:
        if n >= width and char == " ":
            ans.append(x)
            n = 0
            x = ""
        else:
            n = n + 1
            x += char
    return ans


txt, author = getquote()
# Open the image file
img = Image.open(getrandimg()).convert("RGB")

# Create a font object with the desired size
font = ImageFont.truetype("src/font.ttf", size=100)

# Resize the image( Ideal Dimentions for tweet)
ix, iy = 1600, 1400
resized_img = img.resize((ix, iy))

# draw image
I1 = ImageDraw.Draw(resized_img)
# wrap text
wrapped_text = wraptext(txt, 30)

# Print each line of text on the image
w = font.getbbox(text=txt)
line_height = w[3]
nline = len(wrapped_text) + 1
y = iy - (nline * line_height)
y = y / 2
for line in wrapped_text:
    w = font.getbbox(text=line)
    x = ix - w[2] + w[0]
    I1.text((x / 2, y), line, font=font, fill=(255, 255, 255))
    y += line_height
y += line_height
w = font.getbbox(text=author)

x = ix - w[2] + w[0]
I1.text((x / 2, y), author, font=font, fill=(255, 255, 255))


# Display edited image
resized_img.show()


resized_img.save("tweet/post.jpg")
tweet(txt, "tweet/post.jpg")
requests.post(
    "https://api.mynotifier.app",
    {
        "apiKey": "***** Enter API KEY *****",  # This is your own private key
        "message": "Tweeeted SucessFully",  # Could be anything
        "description": txt,  # Optional
        "body": "",  # Optional
        "type": "info",  # info, error, warning or success
        "project": "",  # Optional. Project ids can be found in project tab <-
    },
)
