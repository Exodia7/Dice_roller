## THIS FILE CAN READ INPUT FOR GENERATING DICE ROLLS FOR DICE WITH AN ARBITRARY NUMBER OF SIDES
# There are 3 steps
#   1. parsing the user input
#   2. the actual dice rolls
#   3. printing the results

from random import randint
import re
##from pprint import PrettyPrinter


INT_REG_EXPR = r'^[+-]?\d+$'		# this matches strings that only contains an integer, positive or negative
FLOAT_REG_EXPR = INT_REG_EXPR[:-1] + r'\.\d+$'		# this matches strings that only contain a float, positive or negative
CONST_ID = '0'



def parse_input(input_string):
	""" Parses the provided input string, which should describe a dice roll.
		
		The input should have basic format 
			xdn / xDn
		but can also be the sum of multiple different dice rolls, e.g.
			xdn + ydm + ... + zdl
		and can even contain an additional constant part, such as:
			... + k
		
		where x, n, y, m, z, l and k (so all letters except d) are integers
		
		Input:
			input_string a string in the format described above, describing a (list of) dice roll(s)
		
		Output:
			a dictionary with keys being the maximum value of the dice, and values the number of dices to roll
			AND 
			a integer representing the constant term. Will have value None if it isn't specified
		
		Example:
			for an input_string of '1d20 + 2d3 + 5', the output would for example be:
			{
				'20': 1,
				'3': 2,
			}
			constant = 4
	"""
	#### Pre-process the input string
	parsed = split_string(input_string)
	
	
	#### Loop over all cases
	result = {}
	constant = None
	for dice_roll in parsed:
		# Check how many "d" characters it contains
		num_d_letters = dice_roll.count('d')
		
		if num_d_letters == 0:
			# Then it is a constant, we just need to find what number it is
			if is_int(dice_roll):		# INTEGER NUMBER
				constant = get_as_int(dice_roll)
			##elif is_float(dice_roll):	# FLOAT NUMBER
			##	result[CONST_ID].append(get_as_float(dice_roll))
			else:
				# IN THIS CASE, THE CONSTANT IS NOT GIVEN AS A NUMBER
				## TODO: HOW TO HANDLE THIS CASE
				pass
		
		elif num_d_letters == 1:
			# Then it should be a dice roll, of format xdn, which means:
			#   Roll a dice with n sides x times
			info = [entry.strip() for entry in dice_roll.split('d')]
			
			# Check that the two entries are integers
			if is_int(info[0]) and is_int(info[1]):
				num_dices = get_as_int(info[0])
				num_sides = get_as_int(info[1])
				
				# Set the result to the number of dices we need to roll
				result[num_sides] = num_dices
			else:
				# IN THIS CASE, THE NUMBER OF DICES OR NUMBER OF SIDES IS NOT GIVEN AS AN INTEGER NUMBER
				## TODO: HOW TO HANDLE THIS CASE
				pass
		
		else:
			# IN THIS CASE, THE STRING CONTAINS MULTIPLE 'd'
			## TODO: HOW TO HANDLE THIS CASE
			pass
	
	return result, constant




# TO TEST ? --> should work, quite simple
def split_string(input_string):
	""" Splits the provided string at all "+" symbols
		
		Input: 
			input_string a string that is to be splitted
		
		Output:
			a list of strings, where each string is a part between either 2 "+" symbols, 
			  or 1 "+" symbol and the start/end of the string
	"""
	# Split up on "+"
	parsed = input_string.split('+')
	
	# Remove any leading or trailing space (in case the user didn't type "1d20+5" but "1d20 + 5")
	#  AND put the string to lowercase
	parsed = [part.strip().lower() for part in parsed]

	# And return the result
	return parsed


# TO TEST ? --> should work, quite simple
def roll_dices(num_dices, num_sides):
	""" Roll <num_dices> dices with <num_sides> sides each.
		
		Input:
			num_dices the number of times to roll a dice
			num_sides the number of sides of the dice (= max number the dice can return)
		
		Output:
			a list of the outcomes from the dice rolls
	"""
	outcomes = []
	
	for i in range(num_dices):
		# Compute a random number for the i'th dice
		num = randint(1, num_sides)
		
		# Add it to the list of outcomes
		outcomes.append(num)
	
	return outcomes


# TO TEST
def is_int(input_string):
	""" Checks whether the provided input string is an integer number
	
		Input:
			input_string the string that needs to be checked
		
		Output:
			True or False, corresponding to whether the provided string is an integer number or not.
	"""
	return (re.match(INT_REG_EXPR, input_string) is not None)


# TO TEST
def get_as_int(input_string):
	""" Retrieve the given string and return it as an integer number type.
	
		Note: assumes that the string actually represents an integer.
		
		Input:
			input_string the string to convert to integer type
		
		Output:
			a integer corresponding to the provided input_string
	"""
	return int(input_string)


# TO TEST
def is_float(input_string):
	""" Checks whether the provided input string is a float number (decimal number)
	
		Input:
			input_string the string that needs to be checked
		
		Output:
			True or False, corresponding to whether the provided string is a decimal number or not.
	"""
	return (re.match(FLOAT_REG_EXPR, input_string) is not None)


# TO TEST
def get_as_float(input_string):
	""" Retrieve the given string and return it as a float number type.
	
		Note: assumes that the string actually represents a float.
		
		Input:
			input_string the string to convert to float type
		
		Output:
			a float corresponding to the provided input_string
	"""
	return float(input_string)


# TO TEST
def print_outcomes(dice_rolls, constant):
	""" Displays the resulting dice rolls, the constant term (if any specified),
		as well as the sum of the results to the user.
	
		Input:
			dice_rolls a dictionary of {num_sides: list_of_outcomes} of all requested dice rolls
			constant the constant factor (e.g. "+ 5") if any have been specified by the user.
				If no constant factor was specified, it is set to None
	"""
	total_sum = 0
	num_items = 0
	
	# Go over the dice rolls
	for num_sides, list_outcomes in dice_rolls.items():
		print(f'd{num_sides} roll: ')
		
		for i in range(len(list_outcomes)):
			print(f'  {i+1}. {list_outcomes[i]}/{num_sides}')
			total_sum += list_outcomes[i]
			num_items += 1
		
		print()
	
	# Finally, print the constant factor
	if constant is not None:
		print('And the constant factor being: {constant}')
		total_sum += constant
		num_items += 1
	
	# Only print the total if there is more than one item being summed up
	if num_items > 1:
		print(f'------------------------------------------------------------------\nTOTAL SUM: {total_sum}\n\n')


##### TODO
def print_intro():
	""" Display this program's name in large Ascii art letters,
		and give an introduction to the User.
	"""
	pass


##### TODO
def print_help():
	""" Display the help menu, giving (short) explanations for possible commands,
		and especially the format for the dice rolling
	"""
	print('Dear User, this section still needs to be implemented, sorry. ')
	print('\nAs a general rule, any standard D&D form should work, like e.g. \n  1d20 + 2d6 + 5\n\n')
	


# TO TEST
if __name__ == "__main__":
	##pp = PrettyPrinter()		# FOR DEBUGGING
	

	##### TODO: add an intro explanation
	print_intro()
	
	not_stop = True
	while not_stop:
		# Get the user's input
		input_string = input('Enter the dice roll you want to make (or stop): ').lower()
		print()
		
		if input_string == 'stop':
			not_stop = False
		elif input_string == 'help':
			#### TODO: implement help
			print_help()
		else:
			# Parse the terms
			dice_rolls_to_make, constant = parse_input(input_string)
			
			##print('DEBUG: dice_rolls_to_make:')
			##pp.pprint(dice_rolls_to_make)
			
			# Make the dice rolls
			dice_rolls = {num_sides: roll_dices(num_dice_rolls, num_sides) for num_sides, num_dice_rolls in dice_rolls_to_make.items()}
			
			##print('DEBUG: dice_rolls:')
			##pp.pprint(dice_rolls)
			
			# Finally, print the result
			print_outcomes(dice_rolls, constant)