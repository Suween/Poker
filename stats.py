#!/usr/bin/python

import game as g
import numpy as np
import ui 
from cerberus import Validator
import math 

class Stats:
	__stat_type = ['Wins','Busts','Money','Bust_Slope','Bet_size']

	def __init__(self, game):
		"""
		The stat class collect every stat about the game.
		TODO Complete revamp. no longer give a specific stats to the player, the player get all the stats then choose
		what to do with it
		:param game:
		"""

		if not game:
			print("Instanciation of a Game Class requiere a game Class")
			return

		schema = {'game Type': {'allowed':['Game']}}
		v = Validator(schema)

		if not v.validate({'game Type': [game.__class__.__name__]}):
			print(v.errors)
			print("Allowed Type:" +' Game')

		self.wins = np.empty([0,0])
		self.money = np.empty([0,0])
		self.busts = np.empty([0,0])
		self.b_slope = np.empty([0,0])
		self.bet_size = np.empty([0,0])

		self.bust_slopes_buffer = []
		self.wins_buffer = []
		self.bust_buffer = []
		self.money_buffer = []
		self.bet_size_buffer =[]
		
		self.bjgame = game
		self.numb_of_players = len(self.bjgame.players)

		# When calculating the slope, this is the Dx (over how many point you do the slope)
		self.slope_width = 10 #default

	def update_stats(self):
		"""
		Scan all the player for thiers stats
		:return: NA
		"""

		for players in self.bjgame.players:
			self.wins_buffer.append(players.victory)
			self.money_buffer.append(players.money)
			self.bust_buffer.append(players.bust_count)
			self.bet_size_buffer.append(players.pbet)

			self.differential(self.bust_buffer,self.bust_slopes_buffer,players.bust_count)

	def differential(self, data_buffer, data_slopes_buffer, player_var):
		"""
		Do a derevative of a specific stats
		:param data_buffer: A data array / list
		:param data_slopes_buffer: the data array / list of slopes? Not ever sure myself
		:param player_var: The variable to differentiate
		:return: NA
		"""

		#not sure what this do anymore
		if len(data_buffer) > self.numb_of_players * self.slope_width:
			data_slopes_buffer.append(self.slope(player_var, data_buffer[-((self.numb_of_players * self.slope_width)+1)]))

		elif len(data_buffer) <= self.numb_of_players:
			data_slopes_buffer.append(0)

		else:
			data_slopes_buffer.append(self.slope(player_var, data_buffer[-(self.numb_of_players + 1)]))
			

	def give_stats_to_player(self,stat_type):
		"""
		Give desired stats to a player. The stat they want depends on which playstyle they have
		TODO scrap this
		:param stat_type:
		:return:
		"""

		schema = {'Stat Type':{'allowed': self.__stat_type}}
		v = Validator(schema)

		if not v.validate({'Stat Type':[stat_type]}):
			raise Exception(v.errors,"Allowed Type:" + __stat_type + "for stat type")

		if stat_type == "Bust_Slope":
			return self.bust_slopes_buffer[-(self.numb_of_players)]

		return 0

	def shape_graph(self, buff, array):
		"""
		shape the data list to match the data structure for plotting
		:param buff: Buffers of this class (e.i : bust_slopes_buffer)
		:param array: Something that will be transformed in numpy arrays for matplotlib
		:return:
		"""

		array = np.asarray(buff)
		return np.reshape(array, (len(buff)/self.numb_of_players, self.numb_of_players))

	def shape_for_all_graph(self):
		"""
		Calls the shape graph for the graphs that will be displayed
		:return: NA
		"""

		self.b_slope = self.shape_graph(self.bust_slopes_buffer, self.b_slope)
		# self.busts = self.shape_graph(self.bust_buffer,self.busts)
		# self.wins = self.shape_graph(self.wins_buffer,self.wins)
		self.money = self.shape_graph(self.money_buffer, self.money)
		# self.bet_size = self.shape_graph(self.bet_size_buffer,self.bet_size)

	def show_all(self):
		"""
		Fonction to show all the graphs and all the stats
		:return: NA
		"""

		self.shape_for_all_graph()
		names = self.bjgame.get_players_names()

		# self.show_data("wins",names,self.wins,self.wins_buffer)
		# self.show_data("Busts",names,self.busts,self.bust_buffer)
		self.show_data("Bust Slope",names, self.b_slope, self.bust_slopes_buffer)
		self.show_data("Money", names, self.money, self.money_buffer)
		# self.show_data("bet size",names,self.bet_size,self.bet_size_buffer)

	def show_data(self, label, names, points, buff):
		self.shape_graph(buff,points)
		try :
			graph = ui.Graphs(label,points,names)
			graph.start()
		except ValueError:
			raise(ValueError)

	def slope(self, y2, y1):
		return (y2-y1)
    	

if __name__ == '__main__':

	import deck as d
	import player as p
	
	deck = d.Deck()
	deck.initialize(number_of_card=10,random_order=True)

	player1 = p.Player(player_type = "Gambler", name="Player One")

	game = g.Game(deck)

	game.add_players(player1)#,player2,player3)

	s = Stats(game)