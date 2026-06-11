import streamlit as st
import pandas as pd
from use_db import create_client, use_collection
from use_s3 import create_params, aws_client, get_img           #, s3_exist

params_s3 = create_params()
s3 = aws_client(params_s3)

client = create_client()
collection = use_collection(client)
all_documents = collection.find({}).sort("name", 1)
documents_list = list(all_documents)

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)
sel_doc = None
# altRegMap = None
with col2:
    with st.expander(":blue[Параметри]"):
        altRegMap = st.checkbox(":blue[Альтернативна схема регіонів]")
with col1:
    if altRegMap:
        object_key = "Історичні регіони Львова.png"
    else:
        object_key = "Regions.png"
    img = get_img(s3, params_s3, object_key)
    st.title(":blue[Історичні регіони Львова]")
    st.image(img)
with col2:
    st.subheader(":blue[Виберіть регіон]")
    df = pd.DataFrame(documents_list)
    df_lim = df.iloc[:, 1:2]
    sel = st.dataframe(df_lim, selection_mode="single-row", on_select="rerun")
    sel_rows = sel["selection"]["rows"]
    if len(sel_rows) > 0:
        sel_row = sel_rows[0]
        sel_doc = documents_list[sel_row]
        reg_name = sel_doc.get("name")
        object_key = reg_name + '.png'
        img = get_img(s3, params_s3, object_key)
        st.title(":blue[" + reg_name + "]")
        st.subheader(":blue[Карта регіону]")
        st.image(img)

        with col1:
            reg_spec = sel_doc.get("spec")
            if reg_spec:
                st.subheader("Розташування")
                st.write(reg_spec)
            reg_streets = sel_doc.get("streets")
            if reg_streets:
                st.subheader("Структура")
                st.write(reg_streets)
            reg_hist = sel_doc.get("hist")
            if reg_hist:
                st.subheader("Історія")
                st.write(reg_hist)
            reg_obj = sel_doc.get("obj")
            if reg_obj:
                st.subheader("Цікаві об'єкти")
                st.write(reg_obj)
