# Python Libraries
import requests
import json

class BaseApi():

	def call(self, url, headers):
		r = requests.get(url = url, headers = headers)
		try:
			r.raise_for_status()
		except requests.exceptions.HTTPError as e:
			return e
		
		result = r.json()
		return result

class Budget(BaseApi):

	def __init__(self, headers):
		self._base_url = 'https://api.youneedabudget.com/v1/budgets'
		self._headers = headers
		self._budget = self.call(self._base_url, self._headers)
		self._budget_id = self._budget['data']['budgets'][0]['id']
		self._budget_name = self._budget['data']['budgets'][0]['name']

	def get_budget_id(self):
		return self._budget_id

	def get_budget_name(self):
		return self._budget_name

class Accounts(BaseApi):

	def __init__(self, headers, budget_id):
		self._base_url = 'https://api.youneedabudget.com/v1/budgets/{}/accounts'.format(budget_id)
		self._headers = headers
		self._accounts = self.call(self._base_url, self._headers)
		self._account_list = self._accounts['data']['accounts']

	def get_account_list(self):
		return self._account_list

