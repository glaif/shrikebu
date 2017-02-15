import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer

redirect_uri = 'http://localhost:8080/'
client_secret = 'gnw2abfitiMVAsrsU6vOPs6'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

client = onedrivesdk.get_default_client(
        client_id='a864c29e-ae26-4c91-9e1e-c66b6557d78a', 
        scopes=scopes)

auth_url = client.auth_provider.get_auth_url(redirect_uri)

#this will block until we have the code
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

client.auth_provider.authenticate(code, redirect_uri, client_secret)

def get_children(client, item_id):
    items = client.item(id=item_id).children.get()
    return items

def get_itemid_root(item_name):
    return get_itemid('root', item_name)

def get_itemid(parent_id, item_name):
    children = client.item(id=parent_id).children.get()
    for i in items:
        if i.name == item_name:
            item_id=i.id
            break
    if not item_id:
        print("Error: could not find id of item named %s\n" % (item_name,))
        return None
    return item_id



item_id = "root"
items = get_children(client, item_id)

for i in items:
    print(i.name)
    if i.name == 'backups':
        item_id=i.id
        print(i.id)

items = get_children(client, item_id)
for i in items:
    print(i.name)
