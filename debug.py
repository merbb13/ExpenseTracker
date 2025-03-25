from website.models import User
from website.expense import db
users = User.query.all()
print(users)
