import redis

get_page = __import__('web').get_page
page = 'https://example.com'

inst = redis.Redis()

pg = get_page(page)

print(inst.get("count:{}".format(page)))
print((inst.get(page).decode('utf-8')[:10])+"...")
