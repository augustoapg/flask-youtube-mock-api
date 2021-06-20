import requests

BASE = "http://127.0.0.1:5000"

data = [
    {"name": "Dog Video", "views": 20000, "likes": 19999},
    {"name": "FLASK Tutorial", "views": 1000, "likes": 110},
    {"name": "Random Video", "views": 2000, "likes": 120},
    {"name": "Cat video", "views": 300, "likes": 100},
]

# Test adding new videos
for i in range(len(data)):
    response = requests.put(f"{BASE}/video/{i}", data[i])
    print(response.json())
input()

# Test getting all videos
response = requests.get(f"{BASE}/video")
print(response.json())
input()

# Test deleting a video
response = requests.delete(f"{BASE}/video/2")
print(response.json())

# Test getting a video
input()
response = requests.get(f"{BASE}/video/1")
print(response.json())

# Test getting a video that does not exist
input()
response = requests.get(f"{BASE}/video/21")
print(response.json())

# Test updating a video
input()
response = requests.patch(f"{BASE}/video/0", {"views": 25000, "likes": 24999})
print(response.json())
