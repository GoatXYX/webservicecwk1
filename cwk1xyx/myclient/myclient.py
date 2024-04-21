import requests
from datetime import datetime
import random

session = requests.Session()
def login(url):
    username = input('Username: ')
    password = input('Password: ')
    response = session.post(url, data={'username': username, 'password': password})
    print(response.text)

def logout(url):
    response = session.post(f"{url}/api/logout")
    if response.status_code == 200:
        print(response.text)
    else:
        print('Failed')

def post_story(url):
    headline = input('Headline: ')
    while not headline:
        print('Empty headline not allowed. Enter headline.')
        headline = input('Enter headline: ')
    valid_categories = {'politics', 'entertainment', 'sport', 'technology', 'other'}
    category = input("Enter category ('politics', 'entertainment', 'sport', 'technology', 'other'): ")
    while category not in valid_categories:
        print('Invalid category.')
        category = input("Enter category ('politics', 'entertainment', 'sport', 'technology', 'other'): ")
    valid_regions = {'uk', 'us', 'eu', 'world'}
    region = input("Enter region ('uk', 'us', 'eu', 'world'): ")
    while region not in valid_regions:
        print('Invalid region.')
        region = input("Enter region ('uk', 'us', 'eu', 'world'): ")
    details = input('Enter details: ')
    while not details:
        print('Empty details not allowed. Enter details.')
        details = input('Enter details: ')
    response = session.post(f"{url}/api/stories", json={
        'headline': headline, 
        'category': category, 
        'region': region, 
        'details': details, 
        })
    if response.status_code == 404:
        print('You need to be logged in to proceed with this operation.')
    else:
        print(response.text)
    

def get_stories(command):
    valid_categories = {'politics', 'entertainment', 'sport', 'technology', 'other'}
    valid_regions = {'uk', 'us', 'eu', 'world'}
    valid_commands = {'-id', '-cat', '-reg', '-date'}

    url = 'https://newssites.pythonanywhere.com/api/directory/'
    response = session.get(url)
    if response.status_code == 200:
        agencies = response.json()

    params = {}
    words = command.split()
    invalid_commands = [word.split('=')[0] for word in words if not word.split('=')[0] in valid_commands]
    if invalid_commands:
        print(f"Invalid command. Please enter valid commands: {', '.join(valid_commands)}.")
        return
    agency_id = next((word.split('=')[1] for word in words if word.startswith('-id=')), None)
    if agency_id:
        agencies = [agency for agency in agencies if agency['agency_code'] == agency_id]
    else:
        agencies = random.sample(agencies, 20)  # Random sample if no specific id

    for word in words:
        if word.startswith('-cat='):
            category = word.split('=')[1]
            if category not in valid_categories:
                print('Invalid category.')
                return
            params['cat'] = category
        elif word.startswith('-reg='):
            region = word.split('=')[1]
            if region not in valid_regions:
                print('Invalid region.')
                return
            params['reg'] = word.split('=')[1]
        elif word.startswith('-date='):
            params['date'] = word.split('=')[1]

    all_stories = []
    for agency in agencies:
        try:
            agency_url = f"{agency['url'].rstrip('/')}/api/stories"
            stories_response = requests.get(agency_url, params=params)
            if stories_response.status_code == 200:
                data = stories_response.json()
                stories = data.get('stories', [])
                if 'reg' in params:
                    # Filter stories by region
                    stories = [story for story in stories if story.get('story_region') == params['reg']]
                if 'cat' in params:
                    # Filter stories by category
                    stories = [story for story in stories if story.get('story_cat') == params['cat']]
                if 'date' in params:
                    # Filter stories by date
                    date = datetime.strptime(params['date'], '%Y-%m-%d')
                    stories = [story for story in stories if datetime.strptime(story.get('story_date'), '%Y-%m-%d') >= date]
                all_stories.extend(stories)
            else:
                print(f"Error retrieving stories from {agency['url']}: HTTP {stories_response.status_code}")
        except ConnectionError as e:
            print(f"Error connecting to {agency['url']}: {e}")
    if all_stories:
        for story in all_stories:
            id = story.get('key')
            headline = story.get('headline')
            category = story.get('story_cat')
            region = story.get('story_region')
            author = story.get('author')
            date = story.get('story_date')
            details = story.get('story_details')
            print(f"Key: {id}")
            print(f"Headline: {headline}")
            print(f"Category: {category}")
            print(f"Region: {region}")
            print(f"Author: {author}")
            print(f"Date: {date}")
            print(f"Details: {details}")
            print("-" * 30)
    else:
        print("No stories found.")      
    # response = session.get(agency_url, params=params)
    # if response.status_code == 200:
    #     print('Stories retrieved successfully:')
    #     print(response.json())  # Assumes that the JSON response contains the stories
    # elif response.status_code == 404:
    #     print('No stories found')
    # else:
    #     print(f'Failed to retrieve stories. Status code: {response.status_code}')

def delete_story(command,url):
    story_key = command.split()[1]
    response = session.delete(f"{url}/api/stories/{story_key}")
    
    if response.status_code == 200:
        print(response.text)
    elif response.status_code == 404:
        print('Login first')
    else:
        print('Failed to delete story.')

def register_agency():
    url = 'https://newssites.pythonanywhere.com/api/directory/'
    agency_name = input('Enter name of news agency: ')
    while not agency_name:
        print('Empty agency name not allowed.Enter agency name.')
        agency_name = input('Enter name of news agency: ')
    agency_url = input('Enter the URL of the news agency: ')
    while not agency_url:
        print('Empty agency URL not allowed. Enter the agency URL.')
        agency_url = input('Enter URL of news agency: ')
    agency_code = input('Enter agency code: ')
    while not agency_code:
        print('Empty agency code not allowed. Enter the agency code.')
        agency_code = input('Enter agency code: ')
    response = session.post(url, json={
        'agency_name': agency_name,
        'url': agency_url,
        'agency_code': agency_code
    })
    if response.status_code == 201:
        print('Agency registered successfully.')
    elif response.status_code == 503:
        print(f'Service Unavailable: {response.text}')
    else:
        print(f'An error occurred: {response.text}')

def list_agencies():
    url = 'https://newssites.pythonanywhere.com/api/directory/'
    response = session.get(url)
    if response.status_code == 200:
        agencies = response.json()
        random_agencies = random.sample(agencies, 20)
        for record in random_agencies:
            print(record)
    else:
        print(response.json())
        

    

def main():
    while True:
        command = input('You are in login step, please enter the url:')
        words = command.split() #Split the command by spaces
        if len(words) == 1:
            url = words[0]
            login(url)
            break
    while True:
        command = input('Enter command (login, logout, post, news, delete, list, exit): ')
        words = command.split()
        if len(words) == 1:
            if words[0] == 'exit':
                print('You have exited the program')
                break
            elif words[0] == 'logout':
                logout(url)
            elif words[0] == 'post':
                post_story(url)
            elif words[0] == 'list':
                list_agencies()
            else:
                print('Invalid command')
        elif len(words) == 2:
            if words[0] == 'login':
                url = words[1]
                login(url)
            elif words[0] == 'delete':
                delete_story(command,url)
            else:
                print('Invalid command')
        elif len(words) == 5:
            if words[0] == 'news':
                get_stories(command)
            else:
                print('Invalid command')
        else:
            print('Invalid command')
        


if __name__ == "__main__":
    main()
