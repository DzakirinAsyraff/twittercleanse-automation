import json
from playwright.sync_api import sync_playwright
import time
import os

count = 0
try:
    # Read credentials from file
    with open('credentials.txt', 'r') as file:
        username, password = [line.strip() for line in file]
        print(f'Username: {username}')
        print(f'Password: {password}')
except FileNotFoundError:
    print('Could not find credentials.txt file, creating one...')
    with open('credentials.txt', 'w') as file:
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        file.write(username + '\n')
        file.write(password)
        print('Created credentials.txt file with your credentials')
        exit()
except ValueError:
    print('credentials.txt file is not formatted correctly, please delete it and try again')
    exit()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    
    if os.path.exists('storage_state.json'):
        with open('storage_state.json', 'r') as f:
            storage_state = json.load(f)
        context = browser.new_context(storage_state=storage_state)
    else:
        context = browser.new_context()

    # Create a new page in the context
    page = context.new_page()
    
    # Set no timeout
    page.set_default_timeout(0)

    # Navigate to Twitter login page
    page.goto('https://twitter.com/login')

    # Fill in the username and click Next
    page.fill('input[name="text"]', username)
    page.click('div[role="button"]:has-text("Next")')

    # Wait for navigation to complete
    page.wait_for_load_state("networkidle")
    
    # Wait for the password field to appear
    # page.wait_for_selector('input[name="password"]')
    
    # <input autocapitalize="sentences" autocomplete="current-password" autocorrect="on" name="password" spellcheck="true" type="password" dir="auto" class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7" value="">

    # Fill in the password and submit
    page.fill('input[name="password"]', password)
    page.click('div[data-testid="LoginForm_Login_Button"]')
    print('Logging in...')

    
    
    # After logging in, save the storage state
    storage_state = context.storage_state()
    with open('storage_state.json', 'w') as f:
        json.dump(storage_state, f)
    print('Sleeping for 5 seconds...')
    time.sleep(5)
        
    # Wait for navigation to complete
    page.wait_for_load_state("networkidle")

    # # Navigate to profile page
    # page.goto(f'https://twitter.com/{username}')
    # print(f'Navigated to profile page: https://twitter.com/{username}')
    
    # # Click on the profile link
    # page.click('a[data-testid="AppTabBar_Profile_Link"]')
    # print(f'Navigated to profile page: https://twitter.com/{username}')
    
    
    # # Wait for navigation to complete
    # page.wait_for_load_state("networkidle")
    # print('Network idle in profile page')
    
    # # Wait for the specified class to appear
    # page.wait_for_selector('.css-175oi2r')
    # print('Found the specified class')
    
    # Unfollow all users
    
    # page.goto(f'https://twitter.com/{username}/following')
    # print(f'Navigated to following page: https://twitter.com/{username}/following')
    
    # time.sleep(5)
    
    # while True:
    #     print('Unfollowing users...')
    #     unfollow_buttons = page.query_selector_all('div[data-testid$="-unfollow"]')
    #     if not unfollow_buttons:
    #         print('No more users to unfollow!')
    #         break

    #     for button in unfollow_buttons:
    #         button.click()
    #         # print('Unfollow button')
    #         time.sleep(0.2)  # Wait for the menu to appear
    #         confirm_unfollow_button = page.query_selector('div[role="button"][data-testid="confirmationSheetConfirm"]:has-text("Unfollow")')
    #         if confirm_unfollow_button:
    #             confirm_unfollow_button.click()
    #             print(f'Unfollowed {count} users')
    #             count += 1
    #             time.sleep(0.2)  # Wait for the unfollow action to complete
    #         else:
    #             print('Could not find confirm unfollow button')
    
    # Remove all followers
    
    page.goto(f'https://twitter.com/{username}/followers')
    print(f'Navigated to following page: https://twitter.com/{username}/followers')
    
    time.sleep(5)
    
    while True:
        print('Removing followers...')
        followers = page.query_selector_all('div[aria-label="More"][aria-haspopup="menu"][role="button"]')
        if not followers:
            print('No more followers to remove!')
            break

        for follower in followers:
            follower.click()
            page.wait_for_selector('div[data-testid="Dropdown"]')
            # if there is data-testid="removeFollower" then click on it else skip
            if page.query_selector('div[data-testid="removeFollower"]'):
                remove_follower_button = page.query_selector('div[data-testid="removeFollower"]')
                remove_follower_button.click()
                page.wait_for_selector('div[data-testid="confirmationSheetConfirm"]')
                confirm_button = page.query_selector('div[data-testid="confirmationSheetConfirm"]')
                confirm_button.click()
                print(f'Removed {count} followers')
                count += 1
                time.sleep(0.2)  # Wait for the unfollow action to complete
            else:
                print('Could not find remove follower button')
                page.goto(f'https://twitter.com/{username}/followers')
                page.wait_for_selector('div[data-testid="cellInnerDiv"]')
                
                
                
    # # Remove any reposts from searching my name
    # page.goto(f'https://twitter.com/search?q={username}&src=typed_query')
    # time.sleep(5)
    
    # while True:
    #     # open the tweet
    #     any_tweets = page.query_selector_all('div[data-testid="cellInnerDiv"]')
    #     if not any_tweets:
    #         print('No more tweets to open!')
    #         break
        
    #     for tweet in any_tweets:
    #         tweet.click()
    #         time.sleep(0.2)
    #         # check if it is a repost
    #         repost = page.query_selector('div[data-testid="unretweet"]')
    #         if repost:
    #             print('This is a repost')
    #             # click on the repost button
    #             repost.click()
    #             time.sleep(0.2)
    #             # click on the delete button
    #             delete_button = page.query_selector('div[data-testid="unretweetConfirm"]')
    #             if delete_button:
    #                 delete_button.click()
    #                 print('Deleted repost')
    #                 time.sleep(0.2)
    #             else:
    #                 print('Could not find delete button')
    #         else:
    #             print('This is not a repost')
    #         # move on to the next tweet
    #         page.click('div[data-testid="app-bar-back"]')
    #         time.sleep(5)
            
    # Delete all conversations
    page.goto(f'https://twitter.com/messages')
    time.sleep(5)
    
    while True:
        print('Finding conversations...')
        conversations = page.query_selector_all('div[data-testid="conversation"]')
        # more_buttons = page.query_selector_all('div[aria-label="More"][aria-haspopup="true"][role="button"]')
        if not conversations:
            print('No more conversations to delete!')
            break

        for convo in conversations:
            convo.hover()
            print('Hovering a conversation')
            time.sleep(0.2)
            more_button = page.query_selector('div[aria-label="More"][aria-haspopup="menu"][role="button"]')
            more_button.click()
            time.sleep(0.2)
            options = page.query_selector_all('div[role="menuitem"]')
            delete_button = page.query_selector('div[role="menuitem"]:has-text("Delete")')
            delete_button.click()
            time.sleep(0.2)
            confirm_button = page.query_selector('div[data-testid="confirmationSheetConfirm"]')
            confirm_button.click()
            print('Deleted a conversation')
            
            

    # # Delete all tweets
    # while True:
    #     print('Deleting tweets...')
    #     triple_dot_buttons = page.query_selector_all('div[role="button"][aria-label="More"]')
    #     if not triple_dot_buttons:
    #         print('No more tweets to delete!')
    #         break

    #     for button in triple_dot_buttons:
    #         button.click()
    #         print('Clicked on triple dot button')
    #         time.sleep(1)  # Wait for the menu to appear
    #         delete_button = page.query_selector('div[role="menuitem"]:has-text("Delete")')
    #         if delete_button:
    #             delete_button.click()
    #             print('Clicked on delete button')
    #             time.sleep(1)  # Wait for the delete action to complete
    #             confirm_delete_button = page.query_selector('div[role="button"][data-testid="confirmationSheetConfirm"]:has-text("Delete")')
    #             if confirm_delete_button:
    #                 confirm_delete_button.click()
    #                 print('Confirmed delete action')
    #                 time.sleep(1)  # Wait for the delete action to complete
    #             else:
    #                 print('Could not find confirm delete button')
    #         else:
    #             print('Could not find delete button')

    browser.close()
    print('Done!')