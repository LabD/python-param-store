from itertools import islice

__all__ = [
    'EC2ParameterStore'
]


class BaseStore(object):

    def load_values(self, items):
        raise NotImplementedError()


class EC2ParameterStore(BaseStore):

    def __init__(self):
        import boto3

        self.client = boto3.client('ssm')

    def load_values(self, items):
        """Load the parameters from the AWS Parameter Store

        :parameter items: list with keys
        :rtype: dict

        """
        if not items:
            return {}

        def chunk(it, size):
            it = iter(it)
            return iter(lambda: tuple(islice(it, size)), ())

        iteritems = chunk(items, 10)
        result = {}
        for items in iteritems:
            data = self.client.get_parameters(
                Names=items,
                WithDecryption=True)

            for parameter in data['Parameters']:
                key = parameter['Name']
                value = parameter['Value']
                result[key] = value
        return result
