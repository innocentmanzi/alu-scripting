#!/usr/bin/python3

import requests

def count_words(subreddit, word_list, after=None, count_dict={}):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-Agent': 'Costom'}
    params = {'limit': 100, 'after': after}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        after = data['data']['after']
        
        for post in posts:
            title = post['data']['title']
            title_words = title.lower().split()
            
            for word in word_list:
                word = word.lower()
                if word in title_words and not title.endswith(('.', '!', '_')):
                    if word in count_dict:
                        count_dict[word] += 1
                    else:
                        count_dict[word] = 1
        
        if after is not None:
            count_words(subreddit, word_list, after, count_dict)
        else:
            sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
    else:
        return None

