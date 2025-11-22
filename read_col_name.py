from use_db import create_client, use_collection

client = create_client()
collection = use_collection(client)

all_documents = collection.find({})

documents_list = list(all_documents)
i = 0
for doc in documents_list:
    i += 1
    # st.write(i, doc.get("name"))
    print(i, doc.get("name"))

client.close()
