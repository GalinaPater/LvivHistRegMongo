import streamlit as st
import boto3
import requests
from PIL import Image
from io import BytesIO


def create_params():
    access_key = st.secrets["awsS3"]["access_key"]
    secret_key = st.secrets["awsS3"]["secret_key"]
    region = st.secrets["awsS3"]["region"]
    bucket_name = st.secrets["awsS3"]["bucket_name"]
    params_s3 = {"access_key": access_key, "secret_key": secret_key,
                 "region": region, "bucket_name": bucket_name}
    return params_s3


def aws_client(params_s3):
    access_key = params_s3["access_key"]
    secret_key = params_s3["secret_key"]
    region = params_s3["region"]

    s3 = boto3.client('s3', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key, region_name=region)
    return s3


def get_img(s3, params_s3, object_key):
    bucket_name = params_s3["bucket_name"]
    url = s3.generate_presigned_url('get_object',
                                Params={'Bucket': bucket_name, 'Key': object_key},
                                ExpiresIn=3600)
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def s3_exist(s3, obj_name):
    bucket_name = st.secrets["awsS3"]["bucket_name"]
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=obj_name,
        MaxKeys=1) # Достатньо знайти хоча б один файл
    res = 'Contents' in response
    return res