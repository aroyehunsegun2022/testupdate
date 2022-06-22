from instance.config import MERCHANT_ID


class Config(object):
    MERCHANT_ID='kfjgu'

class ProductionConfig(Config):
    DATABASE_URI=''

class DevelopmentConfig(Config):
    DATABASE_URI=''