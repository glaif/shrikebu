import onedriveapi as oda

REDIRECT_URI = 'http://localhost:8000/'
CLIENT_ID = 'a864c29e-ae26-4c91-9e1e-c66b6557d78a'
CLIENT_SECRET = 'gnw2abfitiMVAsrsU6vOPs6'
SCOPE=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']


#this will block until we have the code
client = oda.OnedriveClient(SCOPE, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET)

def get_children(client, item_id):
#    items = client.item(id=item_id).children.get()
#    return items
    return None

def get_itemid_root(item_name):
    return get_itemid('root', item_name)

def get_itemid(parent_id, item_name):
#    children = client.item(id=parent_id).children.get()
#    for i in items:
#        if i.name == item_name:
#            item_id=i.id
#            break
#    if not item_id:
#        print("Error: could not find id of item named %s\n" % (item_name,))
#        return None
#    return item_id
    return None

#item_id = "root"
#items = get_children(client, item_id)

#for i in items:
#    print(i.name)
#    if i.name == 'backups':
#        item_id=i.id
#        print(i.id)
