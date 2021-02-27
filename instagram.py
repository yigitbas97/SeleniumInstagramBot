from instagramUserInfo import username,password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Instagram:
    def __init__(self,username,password):
        #Browser configuring
        self.browser_locale = 'en'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--lang={}".format(self.browser_locale))
        self.browser = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=self.options)
        
        #User information
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        
        #username and password fields
        usernameInput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
        passwordInput = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
        
        #set values to username and password fields
        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        
        #Press Enter when choosed password field
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(3)

    def getFollowers(self):
        #Go to your instagram page
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(3)
         
        #Count of Total Followers, we use that to determine how many to press space
        totalFollowersCount = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").find_element_by_css_selector("span").text
        print(f"Total Followers Counter : {totalFollowersCount}")

        #Click followers link in your instagram page and then choose all followers
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(3)

        #Take followers with li tag and append list
        followersLinkList = []
        for i in range(1,int(totalFollowersCount) + 1):
            time.sleep(0.5)
            currentFollower = self.browser.find_element_by_xpath(f"/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]")
            followersLinkList.append(currentFollower)
            self.browser.execute_script("arguments[0].scrollIntoView()", currentFollower)

        #Append all followers to list with their instagram user links
        followers = []
        for user in followersLinkList:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            followers.append(link)

        return followers

    def getFollowing(self):
        #Go to your instagram page
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(3)

        #Count of Total Following, we use that to determine how many to press space
        totalFollowingCount = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").find_element_by_css_selector("span").text
        print(f"Total Following Counter : {totalFollowingCount}")

        #Click following link in your instagram page and then choose all following
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        time.sleep(3)

        #Take following with li tag and append list
        followingLinkList = []
        for i in range(1,int(totalFollowingCount) + 1):
            time.sleep(0.5)
            currentFollowing= self.browser.find_element_by_xpath(f"/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]")
            followingLinkList.append(currentFollowing)
            self.browser.execute_script("arguments[0].scrollIntoView()", currentFollowing)

        #Append all following to list with their instagram user links
        following = []
        for user in followingLinkList:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            following.append(link)

        return following

    def nonFollowers(self):
        your_followers = self.getFollowers()
        your_following = self.getFollowing()
        nonFollowersList = []

        for followingUser in your_following:
            if followingUser not in your_followers:
                nonFollowersList.append(followingUser)

        return nonFollowersList

    def followUser(self, username):
        self.browser.get(f"https://www.instagram.com/{username}")
        time.sleep(1)

        followButton = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]").find_element_by_css_selector("button")
        time.sleep(1)

        #Control of button's text
        if followButton.text != 'Unfollow' and followButton.text != 'Requested' and followButton.text != 'Message':
            followButton.click()
            time.sleep(1)
            print("Takip isteği gönderildi !")
        else:
            print("Zaten bu kullanıcıyı takip ediyorsunuz !")

    def unfollowUser(self, username):
        self.browser.get(f"https://www.instagram.com/{username}")
        time.sleep(1)

        #Get All Buttons
        buttons = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]").find_elements_by_css_selector("button")
        time.sleep(1)

        # You are following -> (Message - Unfollow - Suggested - ...) Buttons
        if len(buttons) > 3:
            #Control of button's text
            if buttons[0].text == 'Unfollow' or buttons[0].text == 'Requested' or buttons[0].text == 'Message':
                buttons[1].click()
                time.sleep(2)
                confirmButton = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
                time.sleep(1)
                print("Takipten çıkıldı !")
            else:
                print("Zaten bu kullanıcıyı takip etmiyorsunuz !")

        # You are not following -> (Follow - ...) Buttons
        elif len(buttons) == 2:
            #Control of button's text
            if buttons[0].text == 'Unfollow' or buttons[0].text == 'Requested':
                buttons[0].click()
                time.sleep(2)
                confirmButton = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
                time.sleep(1)
                print("Takipten çıkıldı !")
            else:
                print("Zaten bu kullanıcıyı takip etmiyorsunuz !")

        # You are following -> (Message - Unfollow - ...) Buttons
        else:
            #Control of button's text
            if buttons[0].text == 'Message':
                buttons[1].click()
                time.sleep(2)
                confirmButton = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
                time.sleep(1)
                print("Takipten çıkıldı !")
            else:
                print("Zaten bu kullanıcıyı takip etmiyorsunuz !")


    def unfollowUserWithLink(self, userLink):
        self.browser.get(f"{userLink}")
        time.sleep(1)

        #Get All Buttons
        buttons = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]").find_elements_by_css_selector("button")
        time.sleep(1)

        # You are following -> (Message - Unfollow - Suggested - ...) Buttons
        if len(buttons) > 3:
            #Control of button's text
            if buttons[0].text == 'Unfollow' or buttons[0].text == 'Requested' or buttons[0].text == 'Message':
                buttons[1].click()
                time.sleep(2)
                confirmButton = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
                time.sleep(1)
                print("Takipten çıkıldı !")
            else:
                print("Zaten bu kullanıcıyı takip etmiyorsunuz !")

        # You are not following -> (Follow - ...) Buttons
        elif len(buttons) == 2:
            #Control of button's text
            if buttons[0].text == 'Unfollow' or buttons[0].text == 'Requested':
                buttons[0].click()
                time.sleep(2)
                confirmButton = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
                time.sleep(1)
                print("Takipten çıkıldı !")
            else:
                print("Zaten bu kullanıcıyı takip etmiyorsunuz !")

        # You are following -> (Message - Unfollow - ...) Buttons
        else:
            #Control of button's text
            if buttons[0].text == 'Message':
                buttons[1].click()
                time.sleep(2)
                confirmButton = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
                time.sleep(1)
                print("Takipten çıkıldı !")
            else:
                print("Zaten bu kullanıcıyı takip etmiyorsunuz !")

    def unfollowNonFollowers(self):
        nonFollowers = self.nonFollowers()

        for user in nonFollowers:
            self.unfollowUserWithLink(user)
            time.sleep(0.5)
        
        print("Geri takip etmeyen kullanıcılar takipten çıkıldı !")


instgram = Instagram(username,password)
instgram.signIn()


