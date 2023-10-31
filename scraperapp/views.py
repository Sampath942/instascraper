# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait 


class FollowerList(APIView):
    def insta_login(self,username,password,driver):
        page_url = "https://www.instagram.com/"
        driver.get(page_url)
        time.sleep(5)
        inputs = driver.find_elements(By.TAG_NAME, "input")
        inputs[0].send_keys(username)
        inputs[1].send_keys(password)
        time.sleep(5)
        button = driver.find_element(By.XPATH, "//button[@type='submit']")
        button.click()
        time.sleep(5)
    
    
    def get_followers(self,username,driver):
        driver.get("https://www.instagram.com/"+username+"/followers")
        time.sleep(7)
        # prev_last_follower=''
        # last_follower = driver.find_elements(By.CSS_SELECTOR,"._aacl._aaco._aacw._aacx._aad7._aade")[-1].text
        tot_followers = int(list(driver.find_elements(By.XPATH,"//ul[1]//li")[1].text.split())[0])
        print(tot_followers)
        time.sleep(3)
        anchors=[]
        flag=False
        while len(anchors)!=tot_followers:
            if flag==False:
                for x in range(tot_followers//12 +1):
                    flag=True
                    driver.execute_script('const div = document.getElementsByClassName("_aano")[0];div.scrollTo({top: div.scrollHeight,behavior: "smooth"});')
                    # prev_last_follower=last_follower
                    time.sleep(3)
                    # last_follower = driver.find_elements(By.CSS_SELECTOR,"._aacl._aaco._aacw._aacx._aad7._aade")[-1].text
                    # print("last_follower: ",last_follower)
            else:
                driver.execute_script('const div = document.getElementsByClassName("_aano")[0];div.scrollTo({top: div.scrollHeight,behavior: "smooth"});')
                time.sleep(5)
            

                
            time.sleep(3)   
            anchors = driver.find_elements(By.CSS_SELECTOR,"._aacl._aaco._aacw._aacx._aad7._aade")
            print("hiii",len(anchors))

        followers=[-1]*len(anchors)
        for x in range(len(anchors)):
            followers[x]=anchors[x].text
        print("followers:(%d) "%(len(followers)))
        return followers
    

    def get_following(self,username,driver):
        driver.get("https://www.instagram.com/"+username+"/following")

        time.sleep(7)

        # prev_last_following=''
        # last_following = driver.find_elements(By.CSS_SELECTOR,"._aacl._aaco._aacw._aacx._aad7._aade")[-1].text
        tot_following = int(list(driver.find_elements(By.XPATH,"//ul[1]//li")[2].text.split())[0])
        print(tot_following)
        time.sleep(3)
        anchors=[]
        flag=False
        while len(anchors)!=tot_following:
            if flag==False:
                for x in range(tot_following//12 +1):
                    flag=True
                    driver.execute_script('const div = document.getElementsByClassName("_aano")[0];div.scrollTo({top: div.scrollHeight,behavior: "smooth"});')
                    # prev_last_following=last_following
                    time.sleep(3)
                    # last_following = driver.find_elements(By.CSS_SELECTOR,"._aacl._aaco._aacw._aacx._aad7._aade")[-1].text
                    # print("last_following: ",last_following)
            else:
                driver.execute_script('const div = document.getElementsByClassName("_aano")[0];div.scrollTo({top: div.scrollHeight,behavior: "smooth"});')
                time.sleep(5)

                
            time.sleep(3)
            anchors = driver.find_elements(By.CSS_SELECTOR,"._aacl._aaco._aacw._aacx._aad7._aade")
            print("hiii",len(anchors))
        following=[-1]*len(anchors)
        for x in range(len(anchors)):
            following[x]=anchors[x].text


        print("following:(%d) "%(len(following)))
        return following

    
    def get(self, request, format=None):
        
        instagram_handle = request.query_params.get('handle', None)
        password = request.query_params.get('password', None)
        if instagram_handle!= None:
            l=len(instagram_handle)
            instagram_handle = ''.join(instagram_handle[1:l-1])
        # print(instagram_handle)
        # print(password)
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        driver=webdriver.Chrome(options=options,service=Service(executable_path=r'../../chromedriver'))
        if (password != None):
            l=len(password)
            instagram_handle = ''.join(password[1:l-1])
            self.insta_login(instagram_handle,password,driver)
        else:
            self.insta_login("<Username>","<Password>",driver)
        followers = self.get_followers(instagram_handle,driver)
        following = self.get_following(instagram_handle,driver)
        # followers = ['f1','f2']
        # following = ['f1','f2']
        # print("All followers:", followers)
        # print("All following:", following)
        followers_data = []
        following_data = []
        for x in range(len(followers)):
            followers_data.append({'username': followers[x]})
        
        for x in range(len(following)):
            following_data.append({'username': following[x]})
        
        follower_following = list(set(followers)-set(following))
        following_follower = list(set(following)-set(followers))
        # print(follower_following)
        # print(following_follower)
        follower_following_data = []
        following_follower_data = []

        for x in range(len(follower_following)):
            follower_following_data.append({'username': follower_following[x]})
        
        for x in range(len(following_follower)):
            following_follower_data.append({'username': following_follower[x]})
        
        # print("follower-following",follower_following_data)
        # print("\nfollowing-follower",following_follower_data)

        # Serialize the followers and following data using their respective serializers
        follower_serializer = FollowerSerializer(data=followers_data, many=True)
        following_serializer = FollowingSerializer(data=following_data, many=True)
        follower_following_serializer = Follower_Following_Serializer(data = follower_following_data, many=True)
        following_follower_serializer = Following_Followers_Serializer(data = following_follower_data, many=True)
        serialized_followers={}
        serialized_following={}
        serialized_follower_following={}
        serialized_following_follower={}
        if follower_serializer.is_valid():
            serialized_followers = follower_serializer.validated_data
        if following_serializer.is_valid():
            serialized_following = following_serializer.validated_data
        if follower_following_serializer.is_valid():
            serialized_follower_following = follower_following_serializer.validated_data
        if following_follower_serializer.is_valid():
            serialized_following_follower = following_follower_serializer.validated_data
        response_data = {}

        # Create the response dictionary with separate keys for followers and following
        response_data = {
            "followers": [follower['username'] for follower in serialized_followers],
            "following": [following['username'] for following in serialized_following],
            "followers_following": [follower_following['username'] for follower_following in serialized_follower_following],
            "following_followers": [following_follower['username'] for following_follower in serialized_following_follower],
        }

        return Response(response_data, status=status.HTTP_200_OK)
        
        
