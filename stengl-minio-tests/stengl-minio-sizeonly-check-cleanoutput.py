#######################################
# Progam Name: stengl-minio-md5check.py
# Written By: Je'aime Powell (jpowell@tacc.utexas.edu)
# Original Date: 12/2/21
# Language: Python3
# Purpose: This progam is to be used on UPSTREAM-RPI
#    sensors to test if the provided files exists on 
#    TACC Corral filesystem remotely and if they are the same.
#    Corral Path from Stampede2: /corral/utexas/Stengl-Wyer-Remote-S/S3/
#
# !!!NOTE BEFORE UPLOADING TO REPOSITORY!!!
# Be sure to censor the access and secret keys from the "MiniIO API Setup" Section if written in clear text!
#
# Tested Platforms:
#    - MacOS
#    - RPI400 with Raspbian Buster (32-bit)
#	
# Required Libraries:
#    os - builtin 
#    sys - builtin
#    minio - Installed with "pip3 install minio"
#    dotenv - Installed with "pip3 install python-dotenv"
#
# Usage: "python3 stengl-miniio-md5check.py filepath/filename"
#
# Example output:
#    pi@raspberrypi-dev:~/upstream/stengl-minio-tests $ python3 stengl-minio-md5check.py ../sound/1638493265.wav
#
#    FILE NAME 	| FILE SIZE(bytes) 	| LAST MODIFIED DATE 	| MD5 CHECKSUM
#    -----------------------------------------------------------
#    1638493265.wav 	 1764044 	 2021-12-03 02:35:01.833000+00:00 	 762beb5f700f26346723756002b37e55
#
#    Checking File Sizes and MD5 Checksum's between the local and remote versions of 1638493265.wav
#    Local ---> 1638493265.wav size: 1764044 	 MD5: 762beb5f700f26346723756002b37e55
#    Remote --> 1638493265.wav size: 1764044 	 MD5: 762beb5f700f26346723756002b37e55
#    Looks Good!
########################################

from minio import Minio
import os
import sys

bucketName = 'upstream-recordings'
envPath = '/home/pi/upstream/stengl-minio-tests/.env'

if len(sys.argv) < 2:
  print("\nERROR: Filename and Path Needed \nUSAGE: python3 stengl-minio-sizeonly-check.py path/to/file/filename\n")
  sys.exit()
elif os.path.exists(sys.argv[1]) == False:
  print("\nERROR: File does not exist \nUSAGE: python3 stengl-minio-sizeonly-check.py path/to/file/filename\n")
  sys.exit()

fileName = sys.argv[1]

# Importing API keys from .env file
# Ref: Tutorial https://www.youtube.com/watch?v=YdgIWTYQ69A
# Ref: Dot-env library: https://github.com/theskumar/python-dotenv

from dotenv import load_dotenv
# Imports enviromental variables
load_dotenv(dotenv_path=envPath) 


#######################################
# MiniIO API setup                    #
#######################################
# !!!NOTE BEFORE UPLOADING TO REPOSITORY!!!
# Be sure to censor the access and secret keys from the "MiniIO API Setup" Section if written in clear text!
# This example uses python-dotenv for this purpose with the SERVER, ACCESS_KEY, and SECRET_KEY set in an .env file
# in the same directory as this python file with the format:
#
# SERVER = "server_url:port"
# ACCESS_KEY = "key_for_user"
# SECRET_KEY = "secret_for_user"
#
# If using git/github ensure the .gitignore has ".env" so as to not include it in uploads
#
######################################

# These can be changed to clear text but it is not recommended
SERVER = os.getenv("SERVER")
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")


client = Minio(SERVER, ACCESS_KEY, SECRET_KEY)

objects = client.list_objects(bucketName, prefix='/')

# This bit of code checks the bucket for the uploaded file then shows the size of the local verses the remote file
foundFile = False
for obj in objects:
  if obj.object_name == os.path.split(fileName)[1]:
    foundFile = True
    # Comparing sizes between local and remote files
    #localFileMD5 = os.popen("md5sum %s" %fileName).read()
    if os.path.getsize(fileName) == obj.size: #MD5 not working through minio and ##localFileMD5.split()[0] == obj.etag:
      print("true")
      sys.exit()
      
print("false")
