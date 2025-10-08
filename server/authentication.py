from flask import request
from functools import wraps
from models import Users

def token_required(f):
  @wraps(f)
  def decorated (*args, **kwargs):
    token = None

    if 'Authorization' in request.headers:
      authentication_header = request.headers['Authorization']

      try:
        token = authentication_header.split(" ")[1]
      except IndexError:
          return {'error': 'Token is missing'}, 401

      user = Users.verify_token(token)

      if not user:
        return {'error': 'Token invalid'}, 401

      return f(user, *args, **kwargs)
  return decorated


def instructor_required(f):
  @wraps(f)
  def decorated (user, *args, **kwargs):
    if user.role not in ['admin', 'instructor']:
      return {'error': 'instructor access required'}, 403
    return f(user, *args, **kwargs)
  return decorated

def admin_required(f):
  @wraps(f)
  def decorated (user, *args, **kwargs):
    if user.role != 'admin':
      return {'error': 'admin access required'}, 403
    return f(user, *args, **kwargs)
  return decorated
      