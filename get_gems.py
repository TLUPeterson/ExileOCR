import requests

gem_url = "https://poe.ninja/api/data/itemoverview?league=Crucible&type=SkillGem"

def get_gems():
    words = []
    response = requests.get(gem_url)
    for gem in response.json()['lines']:
        if(gem['name'] not in words):
          words.append(gem['name'])
          
    f = open("gems.txt", "w")
    for word in words:
        f.write(word+"\n")
get_gems()