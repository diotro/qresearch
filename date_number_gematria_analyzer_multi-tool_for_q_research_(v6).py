# Thank you Lord for showing me the answers to reality

"""
Linux (Ubuntu) Installation Instructions:
Linux generally comes preinstalled with Python, so just execute the command below:

sudo apt install -y xclip libncurses5-dev python-pip && pip install --upgrade pip && pip install readline pynput mpmath convertdate clipboard backports.shutil_get_terminal_size

python '/home/user/path/to/multi_tool.py'

---------------------------------------------------

Windows Installation Instructions:
Download and install Python: https://www.python.org/downloads/release/python-2717/

Go to "Edit the system environment variables" in Windows and then click "Environment Variables..."

Select "Path" from System variables and click "Edit..."

Make sure there is a semi-colon on the end of the "Variable value" field, then add "C:\Python27;C:\Python27\Scripts" to it (without quotes). If your folder is not named Python27, change it to what your folder is named.

RESTART your system, and you will now be able to call Python from the Command Prompt.

pip install pynput mpmath convertdate clipboard backports.shutil_get_terminal_size

python "C:\Path\to\multi_tool.py"
"""

#-----------------
# General Imports

try:
	import readline
except ImportError:
	pass

from pynput.keyboard import Key, Controller, Listener
from threading import Thread
import sys

#-----------------
# Imports for date tool

from convertdate import hebrew, mayan, coptic
import datetime as dt

#-----------------
# Imports for number tool

try:
	from sympy.mpmath import mp
except ImportError:
	from mpmath import mp

from bisect import bisect_left
from hashlib import sha256
import math
import itertools

#-----------------
# Imports for gematria tool

#import HTMLParser
#import unicodedata
import clipboard
import codecs

codecs.register_error('replace_with_space', lambda e: (u' ', e.start + 1))

#-----------------------------------------------------------------------
# Introduction

print('\nWelcome to the Date/Number/Gematria Analyzer for Q Research!')

print('        ___  ___  ___  ___ ')
print('       (__ )(__ )(__ )| __)')
print('By      (_ \\ (_ \\ / / |__ \\')
print('       (___/(___/(_/  (___/\n')

print('https://voat.co/v/QRV, https://theprophetictimeline.com/, https://www.reddit.com/r/LightWarriorAscension/\n')

print('How to use:\n')

print('Dates:')
print('     Enter a date in the format of month day year using spaces like so: 10 28 2017')
print('     If info is available for your inputted date, view it like this:    ..10 28 2017')
print('     Calculate the number of days between two dates like this:          10 28 2017 -> 5 14 2020')
print('     Subtract a certain amount of days from a date:                     7 20 2019 - 25999')
print('     Add a certain amount of days to a date:                            12 21 2012 + 2442\n')

print('     When the +, -, or -> function is used, the date on the left side of the screen is assigned')
print('     to a variable called "a", and the date on the right side becomes "b" ... The letter a or b')
print('     can be substituted for a date:\n')

print('     a -> b ....... b - 25999 ....... 11 12 1997 -> a\n')

print('Numbers:')
print('     Input a lone integer to analyze its properties:          541')
print('     After analyzing a number, hit the Right-Shift key to view its next occurrence in Pi')
print('     If info is available for your inputted number, view it like this: ..541\n')

print('     Input an expression to do simple calculations:           1.375 * 1.375')
print('     Add a decimal point to your numbers when doing division: 24576 / 2457.0\n')

print('Pi Search:')
print('     Input a number like so to view its various occurrences in Pi: //2424')
print('     Type anything and press Enter to end search\n')

print('Gematria:')
print('     Input a text message to see the values of the letters, words, and message total: Trump')
print('     Hit the Right-Ctrl key to show the Gematria of text in the Clipboard. This is useful for multi-line messages')
print('     The ciphers used are English Ordinal, Full Reduction, Reverse Ordinal, Reverse Full Reduction')
print('     The fifth gematria value is the sum of all four previous values')

#-----------------------------------------------------------------------
# Number tool

print('\n---------------------------------------------------\n')
print('Generating 99,999 digits of Pi... (Takes about 5 seconds)\n')

pi = ''

mp.dps = 100000
pi = str(mp.pi)[2:][:-3] + '541'	# Remove 2 characters '3.' from the front and remove 3 incorrect digits from the end
max_pi_digits = len(pi)
pi_sample_len = 55					# How many sample digits to get before and after our number

# We now have 99,999 decimal digits of Pi

hash = sha256(pi).hexdigest()

print('SHA256 Hash of 99,999 decimal digits of Pi: ' + hash)

if hash == 'fb547fc33f9cc50f982957fd49011badd8cca43af9e76abf311d875e5b2ba335':
	print('Pi has been correctly computated!\n')
else:
	print('Pi has not been correctly computated.')
	exit()

def find_nth_occurrence_in_pi(num, n):
	position = pi.find(num)
	if position == -1:
		return -1
	while position >= 0 and n > 1:
		position = pi.find(num, position + len(num))
		if position == -1:
			return -1
		n -= 1
	return position

def search_in_pi(num, occurrence_count):

	int_num = int(num)
	num = str(num)
	num_no_leading_zeros = num.lstrip('0')
	pos = find_nth_occurrence_in_pi(num, occurrence_count)

	info_string = ''

	if pos != -1:
		front_var = 0
		back_var = 0

		if pos >= pi_sample_len:
			front_var = pos - pi_sample_len

		if pos > max_pi_digits - pi_sample_len:
			back_var = max_pi_digits
		else:
			back_var = pos + pi_sample_len + len(num)

		sample = pi[front_var:back_var]
		endof = pos + len(num)

		front_amount = endof - front_var - len(num)		# Usually equals pi_sample_len
		sample_front = sample[:front_amount]
		end_amount = len(sample) - len(sample_front) - len(num)
		sample_end = sample[-end_amount:]

		if endof == max_pi_digits:
			sample_end = ''

		sample_string = sample_front + ' ' + num + ' ' + sample_end
		sample_string = sample_string.strip()

		occurrence_string = ' occurrence #' + str(occurrence_count)

		if occurrence_count == 1:
			occurrence_string = ' first'

		info_string = num + occurrence_string + ' appears in Pi at the end of ' + str(endof) + ' digits (Position ' + str(endof + 1) + ') :\n' + sample_string + '\n'
	else:
		info_string = 'This number does not occur within the first 99,999 digits of Pi.\n'

	if int_num <= max_pi_digits:
		selection = pi[:int_num]

		if len(selection) > pi_sample_len:
			selection = selection[-pi_sample_len:]		# Only get last n digits of string

		selection2 = selection + ' ' + pi[int_num : int_num + pi_sample_len]

		info_string2 = '\nWhat occurs at the end of ' + num_no_leading_zeros + ' digits of Pi : \n' + selection2
		info_string2 += '\n' + (' ' * (selection2.find(' '))) + '^'

		info_string += info_string2

	if info_string.endswith('\n'):
		info_string = info_string[:-1]

	return info_string

def find_multiple_pi(num):

	pi_info = search_in_pi(num, 1)

	print('\n\n' + pi_info)

	pi_search_input = ''
	occurrence_count = 2

	pi_search_input = raw_input('')

	while pi_search_input == '':

		pi_info = search_in_pi(num, occurrence_count)

		if 'does not occur' in pi_info:
			return

		print(pi_info)

		pi_search_input = raw_input('')
		occurrence_count += 1

def digit_sum_pi(num):

	count = 0
	digit_sum = 0
	found = False
	zeros = 0

	for digit in pi:
		if found:
			if digit == '0':
				zeros += 1
				continue
			else:
				break

		digit = int(digit)
		digit_sum += digit
		count += 1

		if digit_sum == num:
			found = True
			continue
		if digit_sum > num:
			count = 0
			break

		if count == len(pi) and digit_sum != num:
			count = 0

	count2 = 0
	sum2 = 0

	for digit in pi:
		digit = int(digit)
		sum2 += digit
		count2 += 1

		if count2 == num:
			break

		if count2 == len(pi) and count2 != num:
			count2 = 0

	result_string = ''

	if count != 0:
		result_string += str(count)
		if zeros != 0:
			result_string += ' (up to ' + str(count + zeros) + ')'

		result_string += ' digits of Pi sum to ' + str(digit_sum) + ' ... '

	if count2 != 0:
		result_string += str(num) + ' digits of Pi sum to ' + str(sum2)

	return result_string

def is_perfect_cube(num):
	num = abs(num)
	cube_root = int(round(num ** (1. / 3)))

	if cube_root ** 3 == num:
		return cube_root

	return False

def isPerfect(num, divisors):
	divisors = divisors[:-1]	# All divisors except the number itself

	if sum(divisors) == num:
		return True

	return False

def isRegular(num, factorization):
	if num == 1:
		return True

	for i in factorization:
		if i != 2 and i != 3 and i != 5:	# The factorization of regular numbers only contain 2s, 3s, 5s
			return False

	return True

def isFactorial(num):
	i = f = 1

	while f < num:
		i += 1
		f *= i
	return f == num

def isPerfectSquare(num):
	s = int(math.sqrt(num))
	return s * s == num

def isFibonacci(num):
	return isPerfectSquare(5 * num * num + 4) or isPerfectSquare(5 * num * num - 4)

def divisorGenerator(n):
	large_divisors = []
	for i in xrange(1, int(math.sqrt(n) + 1)):
		if n % i == 0:
			yield i
			if i * i != n:
				large_divisors.append(n / i)
	for divisor in reversed(large_divisors):
		yield divisor

def prime_factors(n):
	i = 2
	factors = []
	while i * i <= n:
		if n % i:
			i += 1
		else:
			n //= i
			factors.append(i)
	if n > 1:
		factors.append(n)
	return factors

def prime_list(n):
	sieve = [True] * n
	for i in xrange(3, int(n ** 0.5) + 1, 2):
		if sieve[i]:
			sieve[i * i::2 * i]=[False]*((n - i * i - 1) / (2 * i) + 1)
	return [2] + [i for i in xrange(3, n, 2) if sieve[i]]

def base10toN(num, base):
	converted_string, modstring = '', ''
	currentnum = num
	if not 1 < base < 37:
		raise ValueError('Base must be between 2 and 36')
	if not num:
		return '0'
	while currentnum:
		mod = currentnum % base
		currentnum = currentnum // base
		converted_string = chr(48 + mod + 7 * (mod > 10)) + converted_string
	return converted_string

def format(line1, line2):
	length = 45
	return line1 + ((length - len(line1)) * ' ') + line2

print('Generating 9,999,999 prime numbers... (Takes about 10 seconds)\n')

biggest_prime = 179424691 # The 10,000,001st prime
second_to_biggest_prime = 179424673
list_of_primes = prime_list(biggest_prime)

print('---------------------------------------------------\n')
print('Program loaded. To exit, type the word exit and hit enter.\n')
print('---------------------------------------------------')

def take_closest(the_list, num):
	pos = bisect_left(the_list, num)
	if pos == 0:
		return the_list[0]
	if pos == len(the_list):
		return the_list[-1]
	before = the_list[pos - 1]
	after = the_list[pos]
	if after - num < num - before:
		return after
	else:
		return before

def prime_info(num):

	if num == 1:
		return 0, 2, 'None', 2		# 2 is the first prime, No previous prime, next prime is 2
	if num == 2:
		return 1, 3, 'None', 3

	number_of_prime = 0
	nth_prime_number = 0
	previous_prime = 0
	next_prime = 0

	if num > 9999999:
		nth_prime_number = 'Unavailable'
	else:
		nth_prime_number = list_of_primes[num - 1]

	if num < second_to_biggest_prime:	# The last prime before the biggest_prime

		if num in list_of_primes:
			number_of_prime = list_of_primes.index(num) + 1
			previous_prime = list_of_primes[number_of_prime - 2]
			next_prime = list_of_primes[number_of_prime]
		else:

			prime = take_closest(list_of_primes, num)

			if num > prime:
				previous_prime = prime
				index = list_of_primes.index(previous_prime) + 1
				next_prime = list_of_primes[index]
			else:
				next_prime = prime # Because the prime is greater than num
				index = list_of_primes.index(next_prime) - 1
				previous_prime = list_of_primes[index]

	else:

		previous_prime = 'Unavailable'
		next_prime = 'Unavailable'

	return number_of_prime, nth_prime_number, previous_prime, next_prime

#-----------------------------------------------------------------------
# Date tool

def get_jd(year, month, day, type = 'julian'):
	if month <= 2:
		year = year - 1
		month = month + 12

	a = int(year / 100)

	if type == 'gregorian':
		b = 2 - a + int(a / 4)
	else:
		b = 0

	jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b -1524.5

	return jd

def split_up_date(date):
	month = int(date.split(' ', 1)[0])
	day = int(date.split(' ', 1)[1].split(' ', 1)[0])
	year = int(date.split(' ', 1)[1].split(' ', 1)[1])

	return year, month, day

def get_coptic_date_information(year, month, day):
	coptic_date = coptic.from_gregorian(year, month, day)

	coptic_year = coptic_date[0]
	coptic_month = coptic_date[1]
	coptic_day = coptic_date[2]

	first_day = coptic.to_gregorian(coptic_year, 1, 1)
	first_day_year = first_day[0]
	first_day_month = first_day[1]
	first_day_day = first_day[2]

	first_date = dt.date(first_day_year, first_day_month, first_day_day)
	second_date = dt.date(year, month, day)
	difference = (first_date - second_date).days

	if difference < 0:
		difference = difference * -1

	day_of_coptic_year = difference + 1

	return str(coptic_month) + '/' + str(coptic_day).replace('.0', '') + '/' + str(coptic_year), day_of_coptic_year

def get_hebrew_date_formatted(year, month, day):
	hebrew_date = hebrew.from_gregorian(year, month, day)

	hebrew_year = hebrew_date[0]
	hebrew_month = hebrew_date[1]
	hebrew_day = hebrew_date[2]

	return str(hebrew_month) + '/' + str(hebrew_day) + '/' + str(hebrew_year)

def get_day_of_hebrew_year(year, month, day):
	hebrew_date = hebrew.from_gregorian(year, month, day)
	hebrew_year = hebrew_date[0]
	hebrew_month = hebrew_date[1]

	first_day = hebrew.to_gregorian(hebrew_year, 7, 1)	# Returns first day of that Hebrew civil year
	first_day_year = first_day[0]
	first_day_month = first_day[1]
	first_day_day = first_day[2]

	first_date = dt.date(first_day_year, first_day_month, first_day_day)
	second_date = dt.date(year, month, day)
	difference = (first_date - second_date).days

	if difference < 0:
		difference = difference * -1

	day_of_civil_year = difference + 1

	# -----

	# Find out what day of the Hebrew Ecclesiastical year it is

	if hebrew_month > 6:
		hebrew_year = hebrew_year - 1

	first_day_e = hebrew.to_gregorian(hebrew_year, 1, 1)  # Returns 1st day of Hebrew Ecclesiastical year
	first_day_year_e = first_day_e[0]
	first_day_month_e = first_day_e[1]
	first_day_day_e = first_day_e[2]

	first_date_e = dt.date(first_day_year_e, first_day_month_e, first_day_day_e)
	second_date_e = dt.date(year, month, day)
	difference_e = (first_date_e - second_date_e).days

	if difference_e < 0:
		difference_e = difference_e * -1

	day_of_ecclesiastical_year = difference_e + 1

	return day_of_ecclesiastical_year, day_of_civil_year

def get_longcount(a):
	return str(a[0]) + '.' + str(a[1]) + '.' + str(a[2]) + '.' + str(a[3]) + '.' + str(a[4])

def get_tzolkin(julian_day):
	tzolkin = mayan.to_tzolkin(julian_day)											# Converts jd to tzolkin: (7, 'Chuwen')
	tzolkin_day_num = mayan._tzolkin_count(tzolkin[0], tzolkin[1])	# Converts (7, 'Chuwen') to day num: 111

	return tzolkin, tzolkin_day_num

def get_date_information(year, month, day):
	jd = get_jd(year, month, day)

	if jd >= 2299171.5:
		jd = get_jd(year, month, day, 'gregorian')

	a = mayan.from_jd(jd)
	julian_day = mayan.to_jd(a[0], a[1], a[2], a[3], a[4])		# Converts Mayan long count to "julian day"

	tzolkin, tzolkin_day_num = get_tzolkin(julian_day)
	long_count = get_longcount(a)

	gregorian_day_of_year = (dt.date(year, month, day) - dt.date(year, 1, 1)).days + 1

	hebrew_date_formatted = get_hebrew_date_formatted(year, month, day)
	day_of_ecclesiastical_year, day_of_civil_year = get_day_of_hebrew_year(year, month, day)

	coptic_date_formatted, day_of_coptic_year = get_coptic_date_information(year, month, day)

	return month, day, year, gregorian_day_of_year, long_count, tzolkin_day_num, tzolkin, hebrew_date_formatted, day_of_civil_year, day_of_ecclesiastical_year, coptic_date_formatted, day_of_coptic_year

def print_date_information(year, month, day, year2, month2, day2, info_available_1, info_available_2):

	month, day, year, gregorian_day_of_year, long_count, tzolkin_day_num, tzolkin, hebrew_date_formatted, day_of_civil_year, day_of_ecclesiastical_year, coptic_date_formatted, day_of_coptic_year = get_date_information(year, month, day)
	nice_date1 = str(month) + '/' + str(day) + '/' + str(year)

	if info_available_1 and info_available_2:
		print('\n\nInformation is available for both dates!')
	elif info_available_1 and year2 == None:
		print('\n\nInformation is available for this date!')
	elif info_available_1 and year2 != None:
		print('\n\nInformation is available for date A!')
	elif info_available_2:
		print('\n\nInformation is available for date B!')

	line1 = 'Date:            ' + nice_date1 + ' (Day ' + str(gregorian_day_of_year) + ')'
	line2 = 'Long count:      ' + long_count
	line3 = "Tzolk'in day:    " + str(tzolkin_day_num) + ' ' + str(tzolkin).replace('"', '')
	line4 = 'Hebrew date:     ' + hebrew_date_formatted + ' (Day ' + str(day_of_civil_year) + ' C, ' + str(day_of_ecclesiastical_year) + ' E)'
	line5 = 'Coptic date:     ' + coptic_date_formatted + ' (Day ' + str(day_of_coptic_year) + ')'

	if year2 == None:

		print('\n')
		print(line1)
		print(line2)
		print(line3)
		print(line4)
		print(line5)

	else:

		month, day, year, gregorian_day_of_year, long_count, tzolkin_day_num, tzolkin, hebrew_date_formatted, day_of_civil_year, day_of_ecclesiastical_year, coptic_date_formatted, day_of_coptic_year = get_date_information(year2, month2, day2)
		nice_date2 = str(month) + '/' + str(day) + '/' + str(year)

		line1_2 = 'Date:            ' + nice_date2 + ' (Day ' + str(gregorian_day_of_year) + ')'
		line2_2 = 'Long count:      ' + long_count
		line3_2 = "Tzolk'in day:    " + str(tzolkin_day_num) + ' ' + str(tzolkin).replace('"', '')
		line4_2 = 'Hebrew date:     ' + hebrew_date_formatted + ' (Day ' + str(day_of_civil_year) + ' C, ' + str(day_of_ecclesiastical_year) + ' E)'
		line5_2 = 'Coptic date:     ' + coptic_date_formatted + ' (Day ' + str(day_of_coptic_year) + ')'

		n = 51

		print('\n')
		print(line1 + (n - len(line1)) * ' ' + '|       ' + line1_2)
		print(line2 + (n - len(line2)) * ' ' + '|       ' + line2_2)
		print(line3 + (n - len(line3) - 2) * ' ' + '[A|B]     ' + line3_2)
		print(line4 + (n - len(line4)) * ' ' + '|       ' + line4_2)
		print(line5 + (n - len(line5)) * ' ' + '|       ' + line5_2)

#-----------------------------------------------------------------------
# Gematria tool

def simplify_text(text):
	text = text.decode('utf-8')
	#text = unicodedata.normalize('NFKD', text)
	#text = HTMLParser.HTMLParser().unescape(text)
	text = unicode(text.encode('utf-8'), encoding='ascii', errors='replace_with_space')
	text = text.encode('ascii', 'ignore').strip()
	text = text.replace("'", '')			# Remove apostrophes so we ignore them
	return text

def Gematria_print(wordnum, letternum, infostring, totalEO, totalFR, totalRO, totalRFR, all_total, EOletters, wordvals, letters):
	done_letters = ''
	done_numbers = ''

	for EOletters_word, letter_word, wordval in itertools.izip(EOletters, letters, wordvals):
		for EOletter, letter in zip(EOletters_word, letter_word):

			done_letters += letter + ' '
			done_numbers += str(EOletter) + ' '

			if len(EOletter) != 1:
					done_letters += ' '

		the_wordval = '(' + str(wordval) + ')  '
		the_spaces = ' ' * len(the_wordval)

		done_letters += ' ' + the_wordval
		done_numbers += ' ' + the_spaces

	complete = ''

	complete += '```\n'
	complete += done_letters + '\n'
	complete += done_numbers + '\n\n'

	all_totals = totalEO + totalFR + totalRO + totalRFR

	complete += '(' + str(totalEO) + ')     ' + '(' + str(totalFR) + ')     ' + '(' + str(totalRO) + ')     ' + '(' + str(totalRFR) + ')     |     (' + str(all_totals) + ')\n\n'

	complete += infostring + '\n'
	complete += '```'

	return complete

def Gematria(text):
	text =  simplify_text(text)

	if not any(c.isalpha() or c.isdigit() for c in text):
		return None, None, None, None, None, None, None, None, None, None, None

	s = ''

	for letter in text:
		if letter.isalpha() or letter.isdigit():
			s += letter
		else:
			if len(s) > 0:
				if s[-1] != ' ':
					s += ' '

	if s[-1] == ' ':
		s = s[:-1]

	words = s.split(' ')

	wordnum = len(words)
	letternum = sum(c.isalpha() for c in s)

	#-----------------

	valuesEO = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8, 'i' : 9, 'j' : 10, 'k' : 11, 'l' : 12, 'm' : 13, 'n' : 14, 'o' : 15, 'p' : 16, 'q' : 17, 'r' : 18, 's' : 19, 't' : 20, 'u' : 21, 'v' : 22, 'w' : 23, 'x' : 24, 'y' : 25, 'z' : 26, '1' : 1,  '2' : 2,  '3' : 3,  '4' : 4,  '5' : 5,  '6' : 6,  '7' : 7,  '8' : 8,  '9' : 9,  '0' : 0}

	valuesFR = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, 'f' : 6, 'g' : 7, 'h' : 8, 'i' : 9, 'j' : 1, 'k' : 2, 'l' : 3, 'm' : 4, 'n' : 5, 'o' : 6, 'p' : 7, 'q' : 8, 'r' : 9, 's' : 1, 't' : 2, 'u' : 3, 'v' : 4, 'w' : 5, 'x' : 6, 'y' : 7, 'z' : 8, '1' : 1,  '2' : 2,  '3' : 3,  '4' : 4,  '5' : 5,  '6' : 6,  '7' : 7,  '8' : 8,  '9' : 9,  '0' : 0}

	valuesRO = {'a' : 26, 'b' : 25, 'c' : 24, 'd' : 23, 'e' : 22, 'f' : 21, 'g' : 20, 'h' : 19, 'i' : 18, 'j' : 17, 'k' : 16, 'l' : 15, 'm' : 14, 'n' : 13, 'o' : 12, 'p' : 11, 'q' : 10, 'r' : 9, 's' : 8, 't' : 7, 'u' : 6, 'v' : 5, 'w' : 4, 'x' : 3, 'y' : 2, 'z' : 1, '1' : 1,  '2' : 2,  '3' : 3,  '4' : 4,  '5' : 5,  '6' : 6,  '7' : 7,  '8' : 8,  '9' : 9,  '0' : 0}

	valuesRFR = {'a' : 8, 'b' : 7, 'c' : 6, 'd' : 5, 'e' : 4, 'f' : 3, 'g' : 2, 'h' : 1, 'i' : 9, 'j' : 8, 'k' : 7, 'l' : 6, 'm' : 5, 'n' : 4, 'o' : 3, 'p' : 2, 'q' : 1, 'r' : 9, 's' : 8, 't' : 7, 'u' : 6, 'v' : 5, 'w' : 4, 'x' : 3, 'y' : 2, 'z' : 1, '1' : 1,  '2' : 2,  '3' : 3,  '4' : 4,  '5' : 5,  '6' : 6,  '7' : 7,  '8' : 8,  '9' : 9,  '0' : 0}

	#-----------------

	totalEO = 0
	totalFR = 0
	totalRO = 0
	totalRFR = 0

	letters = []
	EOletters = []
	wordvals = []

	for word in words:
		wordval = 0
		EOletters_words = []
		letters_words = []

		for letter in word:
			letters_words.append(letter)

			letter = letter.lower()

			wordval += valuesEO[letter]
			EOletters_words.append(str(valuesEO[letter]))

			totalEO += valuesEO[letter]
			totalFR += valuesFR[letter]
			totalRO += valuesRO[letter]
			totalRFR += valuesRFR[letter]

		wordvals.append(wordval)
		letters.append(letters_words)
		EOletters.append(EOletters_words)

	all_total = totalEO + totalFR + totalRO + totalRFR

	infostring = '(' + str(letternum) + ' letters, ' + str(wordnum) + ' words)'

	return wordnum, letternum, infostring, totalEO, totalFR, totalRO, totalRFR, all_total, EOletters, wordvals, letters

#-----------------------------------------------------------------------
# Library

number_library = {
'H1599' : 'H1599 has a root value of 509 because 1599 - 509 = 1090, and 1090 first occurs in Pi directly next to 2209 like so: "1090 2209" ... 499 digits of Pi sum to 2209, and 499 + 2209 = 2708. Then, 4/25/2023 - 2708 days = 11/25/2015, and 11/25/2015 + 1599 days = 4/11/2020. This is the same hint given in the Simpsons as Patty and Selma live in apartment number 1599 at Spinster City Apartments which has an address of 509.',

'G1544' : 'G1544 is the first of 3 words to have a root value of 888 likely because 1544 occurs in Pi like so: "189 1544 11010" ... It appears at the end of 3962 digits which is 1000 more than G2962 "Lord". You can subtract 888 or 1010 days from 7/17/2019, or you can add 189 or 1010 days to 7/17/2019.',

'G2667' : 'G2667 is the second of 5 words to have a root value of 1592. 7777 first appears in Pi at the end of 1592 digits. 12/21/2012 + 2667 days = 4/10/2020 (13.0.7.7.7)',

'G5005' : 'G5005 is the last of 5 words to have a root value of 1592. 7777 first appears in Pi at the end of 1592 digits. The 4th occurrence of 7777 in Pi appears directly next to the first occurrence of 6305 which is 1300 + 5005. The first occurrence of 5005 in Pi appears directly next to the second occurrence of 1300 like so: "1300 5005" ... This is because 9/7/2021 + 1300 days = 3/30/2025, and 3/30/2025 + 5005 days = 12/12/2038',

'12' : '12 is a divine number of perfect order. 12 * 12 = 144, and a group of 144000 are mentioned in The Book of Revelation. The first 144 digits of Pi sum to 666, another very important Pi code.',

'13' : '13 is 1 more than 12, the divine number of perfect balance. 13 is the number of the Cabal, as there are 13 original colonies, 13 Illuminati bloodlines, etc.',

'15' : '15 squared is 225, and 15 cubed is 3375. Every digit of Pi before the "999999" sequence sums to 3375.~15 digits of Pi sum to 77 ... 77 digits of Pi sum to 365 ... 365 digits of Pi sum to 1614',

'17' : '17 is a very important and popular number used in symbolism everywhere. It is the 7th prime. The 17th letter of the alphabet is Q, and "Q" is the name of a god-like being in Star Trek TNG. "Q" is also the name of a military intelligence operation.',

'29' : '29 could represent 2/9/2017, the completion of the 1260 days.',

'30' : '30 is an important number as there are 30 days in a "prophetic month".',

'33' : '33 is the mystical number of Freemasonry. The first repeating number in Pi is 33.',

'34' : '34 is 17 + 17, the value of "Francis" in the name Francis Bacon using the Pythagorean Cipher/Full Reduction Gematria. The first 34 digits of Pi sum to 162 (81 + 81), and 1620 is also an important number relating to the timeline.',

'37' : '37 is the 12th prime number and half of 74.',

'40' : '40 is a very important number mentioned in the Bible many times. The Flood lasted 40 days and 40 nights, the Israelites wandered in the desert for 40 years, Jesus fasted in the wilderness for 40 days, and after Jesus rose from the dead he ministered on Earth for 40 days before ascending. The square of 40 is 1600 which is another very important number relating to the timeline.~The first 40 digits of Pi sum to 192, and 192 has some interesting occurrences in Pi.~An important 40 day period begins on 7/20/2019.',

'42' : '42 is a special number as The Book of Revelation mentions a period of 42 months, or 1260 days. A "prophetic month" is 30 days so 42 * 30 = 1260.~In The Hitchhiker\'s Guide to the Galaxy, "The Answer to the Ultimate Question of Life, The Universe, and Everything" is the number 42.',

'51' : '51 is 17 * 3, and the value of the name "Francis Bacon" in Pythagorean Cipher/Full Reduction Gematria. It is also the number of government facility "Area 51". 51 digits of Pi sum to 249 ... 249 represented in duodecimal is 189 ... 249 digits of Pi sum to 1129, and 1129 is the 189th prime. 189 first occurs in Pi at the end of 1717 digits.',

'71' : '71 is the reverse of 17. The second occurrence of 71 appears at the end of 243 digits of Pi directly next to the first occurrence of 2019. The 243rd birthday of America and the 71st birthday of Israel both take place in the same year, 2019.',

'74' : '74 is an important number and is the value of both "Lucifer" and "Jesus" in English Gematria.',

'81' : '81 is 9 * 9, and 81 * 3 is 243, another relevant number of the timeline. Here is an excerpt from the Masonic Dictionary:~The number nine was consecrated to the Spheres and the Muses. It is the sign of every circumference; because a circle or 360 degrees is equal to nine, that is to say, 3+6+0=9. Nevertheless, the ancients regarded this number with a sort of terror; they considered it a bad presage; as the symbol of versatility, of change, and the emblem of the frailty of human affairs. Wherefore they avoided all numbers where nine appears, and chiefly 81, the produce of nine multiplied by itself, and the addition whereof, 8+1, again presents the number nine.',

'104' : '104 digits of Pi sum to 492 ... 492 digits of Pi sum to 2184 ... 2184 digits of Pi sum to 10000',

'108' : '108 is a special number as Hindu gods have 108 names. There are also 108 stitches on a baseball and 108 cards in an UNO deck. There are 108 days from 1/29/2021, the end of an important 1189 day period to 5/17/2021, a date which is 3069 days from 12/21/2012. The first 3069 digits of Pi sum to 14159.',

'113' : '113 is well known for its part in the fractional approximation of Pi: 355/113 = 3.141592. July 4th, 1776 has the long count of 12.8.0.1.13 and is also the 113th day of the Tzolk\'in.',

'115' : '115 is a noteworthy number as it first appears in Pi at the end of 923 digits, and there are 115 days from 9/23/2017 to 5/31/2017.',

'117' : '117 is most well known for representing the middle chapter of the Bible, which is Psalm 117. It can also represent the middle day (595th day) of an 1189 day period, as the Bible contains 1189 chapters. 4/26/2020 is the middle day of an 1189 day period which starts 9/10/2018, and 4/26/2020 is the 117th day of the year. There are also 426 digits of Pi before the 3rd occurrence of 117.',

'129' : '129 can represent 1/29/2021, which is the end of an important 1189 day period. 10/28/2017 is the first day of that 1189 day period, the day in which Q made hist first post.',

'141' : '141 is one of the well known first couple digits of Pi.',

'144' : '144 is 12 * 12, a very well known number due to its use in The Book of Revelation. The book speaks of a group of 144000 made up of 12000 from 12 tribes. The first 144 digits of Pi sum to 666, a very important Pi key.',

'145' : '145 is well known due to the fact that the 145th prime number is 829, which can represent 8/29/2019, the start of the 1260/1290/1335 days.',

'146' : '146 is a special number because the sum of its divisors is 222, and its representation in octal is also 222. It first occurs in Pi to the right of the "self-locating" number 384 like so: "6521 384 146"~8/29/2019 is the 146th day of the Ecclesiastical Hebrew year, and 146 days after that date is 1/22/2020, the first day of a final 1189 day period to complete the 1335 days.~Also, the first 146 digits of Pi sum to 670, which is the number of days between 7/17/2019 and 5/17/2021',

'150' : '150 can represent 5 "prophetic months" or 30 * 5 = 150.~Revelation 9:10 And they had tails like unto scorpions, and there were stings in their tails: and their power was to hurt men five months.~150 days after the start of the 1260 days on 8/29/2019 is 1/26/2020, the date of Kobe Bryant\'s death.',

'158' : '158 stands out because the 158th prime number is 929, an important number relating to the timeline, the number of chapters in the Old Testament. 158 days after February 9th is July 17th, unless it is a leap year.',

'159' : '159 is one of the well known first couple digits of Pi. The reverse of 159 is 951 which represented in octal is 1667.',

'162' : '162 is 81 + 81, and 1620 is an important number relating to the timeline, occurring at the end of 1327 digits.~"The Major League Baseball (MLB) season schedule consists of 162 games for each of the 30 teams in the American League (AL) and National League (NL), played over approximately six months"',

'173' : '173 is the 40th prime number, and the number of chapters in the 1611 KJV Apocrypha. Ezekiel 17:3 is the only verse in the original 1611 KJV Bible that contains an apostrophe. This verse contains an important code relating to the 1260 days.',

'187' : '187 is a special number which relates to the date 7/26/2020. 229 first appears in Pi at the end of 187 digits in this very special location: "2294895"~7/26/2020 - 2294 days = 4/15/2014~7/26/2020 + 187 days = 1/29/2021',

'189' : '189 is a very special number because it first appears in Pi at the end of 1717 digits. This is synchronistic as 189 days after 7/17/2019 is another very important date on the timeline. 189 days can also be added to 7/24/2020, the completion of the 1150 days/2300 sacrifices from The Book of Daniel. A commonly cited statistic is that there are 189 Jesuit institutions of higher learning throughout the world.',

'192' : '192 is an interesting number as the first 40 digits of Pi sum to it. Its third occurrence appears in Pi at the end of 1620 digits, 4th occurrence at end of 1735 digits, 5th occurrence at end of 2899 digits, and 6th occurrence at end of 2946 digits; all numbers which have a strong relation to the timeline.',

'222' : '222 is a very important number which relates to the timeline. 7/20/2019 is the end of the 7920 days, and is the 222nd day of the Tzolk\'in. 2/9/2023 is the end of the 1260 days and is also the 222nd day of the Tzolk\'in. 5/31/2017 is the start of the 1150 days and is the 222nd day of the Tzolk\'in as well.~9/11/2001 takes place 1399 days after the start of the 7920 days on 11/12/1997. 1399 is the 222nd prime number, and the reverse, 9931, first appears in Pi at the end of 22222 digits.~222 first appears in Pi at the end of 1737 digits, and 12/21/2012 + 1737 days = 9/23/2017, the date of the "Revelation 12 Sign".~It is also noteworthy that the first 222 digits of Pi sum to 1005, another very important Pi key.',

'223' : '223 is the 48th prime number and could be seen as a complimentary number to 556, as 556 + 223 = 779. Either 223 or 779 days can be added to 8/29/2019 to arrive at interesting dates. 223 days after 8/29/2019 is 4/8/2020, Passover, a date which is 26262 days after the founding of Israel. Israel was also founded on the 223rd day of the Tzolk\'in.~556 and 223 were the numbers encoded into Isaac Kappy\'s unlocked final message: "July 4th 2019 THE Return of the King Return to THE LIGHT"',

'225' : '225 is 15 squared, and a divisor of 3375, which is the sum of every digit of Pi before the "999999" sequence. 225 days after 8/29/2019 is 4/10/2020, the tenth day of 10 days from Revelation. 4/8/2020 is also the 225th day of the Tzolk\'in. 2665 digits precede the 225th prime (1427) in Pi, as 12/21/2012 + 2665 days = 4/8/2020',

'229' : '229 is a special number as Greek word G229 is used in two Bible verses which seem to depict a rapture type scenario. 229 first appears in Pi at the end of 187 digits in this very special location: "2294895"~7/26/2020 - 2294 days = 4/15/2014~7/26/2020 + 187 days = 1/29/2021',

'232' : '232 is a very important number relating to the timeline. The 232nd prime number is 1459, and 232 + 1459 = 1691. The 691st prime number is 5189 which first appears in Pi at the end of 1717 digits.~4/11/2020, the completion of 10 days mentioned in Revelation, is 232 days from 11/29/2020, which is the 1129th day of a period which starts 10/28/2017.',

'234' : '234 first occurs in Pi at the end of 262 digits. It is 117 + 117.',

'241' : '241 could be representative of 8/29/2019 or 5/31/2017. 8/29/2019 is the 241st day of the year, and 5/31/2017 is the 241st day of the Hebrew Civil Year. 241 days after 8/29/2019 is a very important date on the timeline, 4/26/2020. 241 days after 5/31/2017 is 1/27/2018 (11/11/5778)',

'243' : '243 is 81 * 3, and 81 is 9 * 9. Here is an excerpt from the Masonic Dictionary:~The number nine was consecrated to the Spheres and the Muses. It is the sign of every circumference; because a circle or 360 degrees is equal to nine, that is to say, 3+6+0=9. Nevertheless, the ancients regarded this number with a sort of terror; they considered it a bad presage; as the symbol of versatility, of change, and the emblem of the frailty of human affairs. Wherefore they avoided all numbers where nine appears, and chiefly 81, the produce of nine multiplied by itself, and the addition whereof, 8+1, again presents the number nine.~The first occurrence of 271 and the second occurrence of 71 in Pi appear at the end of 243 digits. The 243rd birthday of America, 7/4/2019, is an important landmark on the timeline, being 297 steps up from 9/10/2018, the start of an important 1189 day period. The 243rd birthday of America and the 71st birthday of Israel both take place in the same year, 2019.',

'255' : '255 first appears in Pi at the end of 1170 digits, directly next to the first occurrence of the number 319 (11 * 29). 255 could be seen as the number of days from 3/19/2020 (Spring Equinox) to 11/29/2020.',

'260' : '260 is an extremely important number which relates to the timeline, as there are 260 days in the Mayan Tzolk\'in Cycle. There are 929 chapters in the Old Testament and 260 chapters in the New Testament of the Bible. 929 and 260 are complimentary numbers which form a very important number 1189.~The first occurrence of 360 and 260 appear in Pi 1 digit apart from each other like so: "360 7 260~5/14/2020 -> 1/29/2021 = 260 days"',

'262' : '262 is highly aligned with Pi because the 262nd prime number is 1667, and the 1667th prime number is 14159. Then, 262 + 1667 = 1929, and 929 is the number of chapters in the Old Testament.~10/28/2017 -> 5/14/2020 = 929 days~12/26/2014 -> 9/14/2015 = 262 days~7/17/2019 -> 4/4/2020 = 262 days~5/14/1948 -> 4/8/2020 = 26262 days~262 could also represent 4/12/2015 which has the Mayan long count of 13.0.2.6.2 ... This day is the 222nd day of the Tzolk\'in, and is a multiple of 260 days from any other 222 day.',

'265' : '265 is one of the well known first couple digits of Pi. Pi is "3.14159 265". 1697 is the 265th prime number, and the first 1697 digits of Pi sum to 7661. The reverse of 7661 is 1667, and the 1667th prime number is 14159. There are 265 days from 7/20/2019 to 4/10/2020.~265 digits of Pi sum to 1201 ... 1201 digits of Pi sum to 5404~Hebrew word H5404 means "Eagle" and is code for:~11/12/1997 -> 8/29/2012 = 5404 days~265 could also represent 4/15/2015 which has the Mayan long count of 13.0.2.6.5 ... This day is 777 days from 5/31/2017 and 6363 days from 11/12/1997.',

'271' : '271 is the 10th centered hexagonal number. 271 could be seen as the counterpart to 541, as 541 is the 10 star number, and removing the points of the star gives you 271.~271 first appears in Pi at the end of 243 digits, directly next to the first occurrence of the number 2019. This could represent how the 243rd birthday of America and the 71st birthday of Israel both take place within the same year, 2019.~271 can also represent 9/28/2021, a date which is 761 days after the start of the 1260 days from Revelation. 9/28/2021 is the 271st day of the year and is the 243rd day of the Tzolk\'in. It\'s important to mention that the second occurrence of 271 in Pi appears directly next to the number 4526.~9/28/2021 + 4526 days = 2/18/2034 (13.1.1.8.9)',

'289' : '289 is a very important number relating to the timeline, as it is 17 * 17. Examples of dates that are 289 days from each other:~11/25/2017 - 289 days = 2/9/2017~11/25/2017 + 289 days = 9/10/2018~9/10/2018 + 578 days (289 * 2) = 4/10/2020~4/10/2020 + 289 days = 1/24/2021 (11/11/5781)~2/9/2023 + 289 days = 11/25/2023 (13.0.11.1.11)',

'293' : '293 can refer to the number of days from 4/11/2020 to 1/29/2021.',

'294' : '294 is an extremely important and blatant Pi code which relates to the timeline. 294 occurs directly next to the number 895 in Pi, and these are the first two numbers to occur directly next to each other while summing to 1189, the number of chapters in the Bible. 294 refers to the date 4/10/2020 (13.0.7.7.7), a date which is 294 days from the end and 895 days from the beginning of an important 1189 day period. This date is the 10th and final day of a period of 10 days mentioned in The Book of Revelation. You can also add 294 days to 1/22/2020, the start of another important 1189 day period, to arrive at 11/11/2020.~294 digits of Pi sum to 1319 ... 1319 digits of Pi sum to 5957~If you add 5957 days to 10/28/2017, which is the start of an 1189 day period, you arrive at 2/18/2034 (13.1.1.8.9)',

'297' : '297 is a very important number which makes up an 1189 day period. It is 3 * 3 * 33~297 + 297 + 1 + 297 + 297 = 1189, the number of chapters in the Bible.~9/10/2018 is the start of a very important 1189 day period, and if you add 297 days to that date, you arrive at 7/4/2019, the 243rd birthday of America, a very important landmark on the timeline.~You can also add 297 days to 7/24/2020 to arrive at a special date, 5/17/2021.',

'311' : '311 could represent 3/11/2023, the completion of the 1290 days.',

'315' : '315 is one of 3 very special three-digit "self-locating" numbers of Pi. The first occurrence of 315 in Pi appears at the end of 315 digits. The date 11/11 is the 315th day of the year except on leap years. The 243rd birthday of America is 315 days from the 72nd birthday of Israel:~7/4/2019 -> 5/14/2020 = 315 days',

'319' : '319 is 11 * 29 and could be seen as the number which represents the Spring Equinox on 3/19/2020. The first occurrence of 319 and 255 in Pi appear directly next to each other, and 255 days from 3/19/2020 is 11/29/2020, the 1129th day of a very special period of time.',

'323' : '323 is one of the well known first couple digits of Pi. March 23rd is the birthday of Lord Pakal, the self-proclaimed messenger of the time cycles.~If you add 323 days to 3/23 you will always arrive at February 9th of the next year, another very important day on the timeline.~If you add 189 days to 3/23/2021 you arrive at 9/28/2021.~If you add 323 days to the 71st birthday of Israel on 5/14/2019, you arrive at 4/1/2020, the first of 10 days from Revelation.',

'334' : '334 intersects 446 in Pi like so: "33446". The addition of 334 to 446 is 780 which is 260 * 3.~334 days after 5/31/2017 is 4/30/2018, the second day of the 70 weeks of Daniel, a date which is 7474 days after the start of the 7920 days on 11/12/1997. 4/30/2018 is also 446 days before the completion of the 7920 days on 7/20/2019.',

'333' : '333 first appears in Pi at the end of 1700 digits. 333 could be representative of 7/26/2020, which is the 333rd day of the 1260 days from Revelation which begin 8/29/2019. 7/26/2020 is also the 1700th day of another period of time. There are 333 digits of Pi before the first occurrence of the number 829, which appears as: "8292540". What\'s interesting is that 7/26/2020 takes place 8292 days after the start of the 7920 days on 11/12/1997.~The first 333 digits of Pi sum to 1482, and 1482 days after 12/21/2012 is 1/11/2017, a date which is 917 days from 7/17/2019.',

'336' : '336 is noteworthy as 829, a number which can represent 8/29/2019 (the start of 1260 days), first appears in Pi at the end of 336 digits. The first 336 digits of Pi sum to 1501, and 8/29/2019 - 1501 days = 7/20/2015, a very significant date on our timeline.',

'354' : '354 first appears in Pi at the end of 701 digits, directly next to the second occurrence of the number 2019. There are 354 days in Hebrew Civil Year 5778, and if you add 354 days to 9/9/2018, the 354th and final day of 5778, you arrive at 8/29/2019, the start of 1260 days from the Book of Revelation.',

'355' : '355 is well known for its part in the fractional approximation of Pi: 355/113 = 3.141592 ... 355 is half of the important Pi key 710, and has a cosine of -0.999999999',

'357' : '357 can represent 7/17/2019, a date which is 357 days after the start of the final 360 day cycle which makes up the 7920 days. 7/17/2019 is also 2399 days after 12/21/2012, and 2399 is the 357th prime number.',

'358' : '358 can represent 7/17/2019, as that date is the 358th day of the final 360 day cycle which makes up the 7920 days. 358 occurs at the end of only 11 digits of Pi, and is seen as 717 in 2Pi. The second occurrence of 358 in Pi appears only 1 digit away from the first occurrence of 7918, as the 7918th day of the 7920 days is 7/17/2019. It is also worth noting that the first 358 digits of Pi sum to 1600, another important number of the timeline.',

'360' : '360 is a very special number, as there are 360 degrees in a circle and 360 days in a "Prophetic Year" or the Mayan Tun unit. 360 has its first occurrence in Pi one digit away from the first occurrence of 260, as there are 260 days in the Mayan Tzolk\'in. Also, 360 represented in duodecimal is 260.~360 is one of 3 very special three-digit "self-locating" numbers of Pi. The second occurrence of 360 in Pi appears at the end of 360 digits.',

'369' : '369 is a very special number which first occurs in Pi at the end of 1554 digits. 1554 is 777 + 777. The first 369 digits of Pi sum to 1622. If you add 1622 days to 12/21/2012, you arrive at 5/31/2017, the start of the 1150 days from Daniel. 5/31/2017 is also 777 days from 7/17/2019. 777 days before 5/31/2017 is also a significant date.~1/26/2020 -> 1/29/2021 = 369 days',

'373' : '373 is the 74th prime number, and 74 is the value of "Jesus" and "Lucifer" in English Gematria. Here are examples of dates which are 373 days apart:~7/17/2019 -> 7/24/2020 = 373 days~1/22/2020 -> 1/29/2021 = 373 days~4/2/2022 (13.0.9.7.9) (1/1/5782) -> 4/10/2023 = 373 days',

'384' : '384 is one of 3 very special three-digit "self-locating" numbers of Pi. The third occurrence of 384 in Pi appears at the end of 384 digits. It occurs in Pi at this very special position: "6521 384 146 9 519". 6521 is the number of days from 9/11/2001 to 7/20/2019. It is also interesting to note that the reverse of 384 is 483, which is the three digit number which takes the longest to have its first occurrence in Pi. 483 first occurs in Pi at the end of 8555 digits.~384 first occurs in Pi like so: "14159 265 358 979 32 384"~384 digits of Pi sum to 1688, and 1688 + 979 is 2667, the number of days from 12/21/2012 to 4/10/2020.',

'390' : '390 is an interesting number as 951 first appears in Pi at the end of 390 digits. 951 is represented in octal as 1667. Then, 390 first appears in Pi at the end of 1189 digits.',

'415' : '415 is one of the well known first couple digits of Pi, and can represent April 15th. On April 15th Abraham Lincoln was assassinated, the Titanic sunk, the Boston Bombing occurred, and the Notre-Dame Cathedral was burned. "Tax Day" also typically takes place on 4/15. From 2/9/2017 to 12/25/2020 is 1415 days.~4/15/2014 is the date of the first blood moon of a special tetrad of blood moons, and can be seen as the middle day/595th day of an important 1189 day period which begins 8/29/2012. 595 first occurs in Pi at the end of 415 digits.~Greek word G415 is one of five words in the New Testament to have a root value of 989, which represents the end of an age.~4/15/2014 -> 7/26/2020 = 2294 days',

'420' : '420 is well known in the Cannabis Community, but has a notable relation to the date 4/10/2020. 953 first occurs in Pi at the end of 420 digits, and 8185 has its first occurrence at the end of 953 digits. 11/12/1997 + 8185 days = 4/10/2020',

'424' : '424 is a very important number relating to the timeline, and first occurs in Pi at the end of 1111 digits. The number of Jesus, 2424, also resides at the end of 1111 digits. 424 can represent 4/24/2023, which is the final day of the 1335 days from Daniel. This is notable as the final day of a 1144 year period of time takes place on 11/11/1997. In addition to this, the last day of World War I took place on 11/11/1918.',

'425' : '425 could represent 4/25/2023, the completion of the 1335 days.',

'426' : '426 is well known for representing 4/26/2020, the middle day/595th day of an important 1189 day period which begins on 9/10/2018. 8/29/2019 is the start of the 1260 days from Revelation, and is the 241st day of the year. 241 days after this date is 4/26/2020. 4/26/2020 is also the 117th day of the year, as the middle chapter of the Bible is Psalm 117. It may be worth noting that the 77th prime is 389 and the 389th prime is 2683.~12/21/2012 + 2683 days = 4/26/2020',

'429' : '429 could represent 4/29/2018, the first day of the 70 weeks/490 days from The Book of Daniel. 429 occurs at the end of 1231 digits of Pi, and 4/29/2018 + 1231 days = 9/11/2021, the first day of Coptic year 1738, and the 20th anniversary of 9/11.~It is interesting to note that the first day of the 70 weeks is 4/29/2018 and the last day is 8/31/2019. 429 + 831 = 1260, and 1260 is another very important number of the timeline.',

'444' : '444 first appears in Pi at the end of 2709 digits, and 2709 is one off from important Pi key 2708, which is 499 + 2209.',

'446' : '446 intersects 334 in Pi like so: "33446". The addition of 334 to 446 is 780 which is 260 * 3.~334 days after 5/31/2017 is 4/30/2018, the second day of the 70 weeks of Daniel, a date which is 7474 days after the start of the 7920 days on 11/12/1997. 4/30/2018 is also 446 days before the completion of the 7920 days on 7/20/2019.',

'483' : '483 is the three digit number which takes the longest to have its first occurrence in Pi. This means that every other 3 digit number has at least one occurrence in Pi before the first occurrence of 483. 483 first occurs in Pi at the end of 8555 digits.~Daniel mentions a 70 week period of time and breaks up the 70 weeks into 7 weeks + 62 weeks + 1 week. From the start of the 70 weeks of Daniel on 4/29/2018 to the first day of the final week on 8/25/2019 is 483 days.~483 digits of Pi sum to 2141, which is the 323rd prime number.~The reverse of 483 is 384, which occurs at the end of 384 digits of Pi.~384 digits of Pi sum to 1688 ... 1688 digits of Pi sum to 7621 (7, 62, 1 ?)~483 can also represent 5/12/2017 which has the long count of 13.0.4.8.3~1/17/2019 (11/11/5779) + 483 days = 5/14/2020~7/17/2019 + 483 days = 11/11/2020~12/25/2020 -> 4/22/2022 (13.0.9.8.9) = 483 days',

'484' : '484 is a special Pi key which has its first occurrence in Pi at the end of 2365 digits, which can represent 2365 days after 12/21/2012, which is 6/13/2019, the 594th day of an 1189 day period, or the last day/297th day of a 297 day segment in an 1189 day period.~The second occurrence of 484 in Pi is at the end of 2772 digits, to represent the number of days from 12/21/2012 to 7/24/2020, the completion of the 1150 days of sacrifice from The Book of Daniel. 484 has its third occurrence in Pi as the number "4848" which appears directly next to the first occurrence of the number 1005, which represents how 1005 days are needed starting 7/24/2020 to complete the 1335 days from Daniel. 4848 can be seen as double 2424, the number of Jesus, as Jesus sacrificed himself on the cross.~5/2/2018 -> 8/29/2019 = 484 days',

'487' : '487 is a very important number which represents the number of days from the start of the 70 weeks of Daniel on 4/29/2018 to the first day of the 1260 days on 8/29/2019. 487 first occurs in Pi at the end of 2650 digits (265 * 10). It appears in a very important area which is rich in important codes: "216 829 989 487 2265 880"',

'490' : '490 is most well known for representing the number of days which makes up the 70 week period of time mentioned in The Book of Daniel.',

'492' : '492 can represent 5/31/2017 which has the long count of 13.0.4.9.2 ... 492 is an interesting number because of the following sequence:~104 digits of Pi sum to 492 ... 492 digits of Pi sum to 2184 ... 2184 digits of Pi sum to 10000~5/31/2017 is 2860 days from 3/30/2025, which is 10000 days after 11/12/1997.',

'499' : '499 is a very special number which relates to the timeline. 499 represented in octal is 763, and 499 first occurs in Pi at the end of 763 digits. Here are some examples of well known dates on the timeline which occur 499 days apart:~9/28/2021 -> 2/9/2023 = 499 days~9/10/2018 -> 1/22/2020 = 499 days~12/12/2021 -> 4/25/2023 = 499 days~499 digits of Pi sum to 2209~12/12/2021 - 2209 days = 11/25/2015~499 + 2209 = 2708, another very important timeline code in Pi.~499 is the 95th prime and it is worth mentioning that the date of the publication of Martin Luther\'s 95 Theses is aligned with 9/28/2021.',

'512' : '512 in binary is 1000000000, and 512 squared is 262144 which seems noteworthy as 262 and 144 are both important Pi codes. 512 can represent 5/12/2017 which has the special long count: 13.0.4.8.3 ... This day is the 222nd day of Hebrew Civil Year 5777, and is 1600 days away from another important landmark, 9/28/2021.',

'514' : '514 could represent 5/14/1948, the date of the founding of Israel. 514 first occurs in Pi directly next to the first occurrence of the number 3996 which is 666 * 6.',

'517' : '517 first occurs in Pi at the end of 2110 digits or at position 2111. 517 is like a combination of 51 and 17, as 51 is 17 * 3. 517 could represent 5/17/2021, a day which is 3069 days after 12/21/2012, as the first 3069 digits of Pi sum to 14159.',

'519' : '519 is 173 * 3, and there are 173 chapters in the 1611 KJV Apocrypha. Double 519 is 1038, which first occurs in Pi directly next to "7777". 519 has its first occurrence in Pi only 1 digit from the first occurrence of 146, as these are both numbers which can be added to 8/29/2019. Adding 146 days brings you to the beginning of an 1189 day period, and adding 519 days brings you to the end of an important 1189 day period.',

'529' : '529 is 13 squared, and 5/29/1917 is JFK\'s birthday.',

'531' : '531 represents 5/31/2017, the start date of the 1150 days from The Book of Daniel. Once the 1150 days are completed, 1005 more days are needed to complete the 1335 days. 531 first occurs in Pi at this special position: "531 910 4848 1005"~Greek word G531 is used only in Hebrews 7:24 as code that 5/31/2017 and 7/24/2020 are the start and end dates of the 1150 days.~The number 23:50 represents 11:50 in 24 hour time. The first Q post which contains the timestamp 23:50 is Q post number 531. The next time that "23:50" appears in the timestamp field is Q post number 724.~The number 777 is used only in Genesis 5:31 which says "And all the days of Lamech were seven hundred seventy and seven years: and he died." ... This is because 777 days after 5/31/2017 is another important date, 7/17/2019.',

'533' : '533 can sometimes represent 17 months and 17 days:~10/16/2021 -> 4/2/2023 = 533 days~2/9/2019 -> 7/26/2020 = 533 days~113 digits of Pi sum to 533',

'540' : '540 appears by the first occurrence of 829 in Pi. 540 * 2.2 = 1188 ... 540 represented in duodecimal is 390, which occurs at the end of 1189 digits of Pi.',

'541' : '541 is the 100th prime number, 10th star number, and the value of the Hebrew word for "Israel" in the Old Testament. 541 first occurs in Pi directly next to 2424, the number of Jesus. The 541st prime is 3911, another important Pi code.~The 3rd occurrence of 541 in Pi appears at the end of 3125 digits, which is 5^5 ... The 4th occurrence is at the end of 4160 digits, which is 9 * 9 * 9 * 9 - 7 * 7 * 7 * 7 ... The 7th occurrence appears at the end of 5280 digits, the number of feet in a mile.~9/23/2017 -> 12/12/2021 = 1541 days',

'550' : '550 is an important number relating to the timeline. The 550th prime is 3989 which occurs in a special palindrome in Pi. There are 550 days from 9/7/2021, the middle day of a final 1189 day period, to 3/11/2023, the completion of the 1290 days.',

'552' : '552 is an important Pi key which first occurs in Pi at the end of 1665 digits. 12/26/2014 is the start of an important period of time. The 552nd day of this period is 6/29/2016. The 1665th day of this period is 7/17/2019. This is special as the first occurrence of 629 and 717 in Pi appear directly next to each other.~The first 552 digits of Pi sum to 2443, which could represent how the 2443rd day of the 14th baktun is 8/29/2019, the first day of the 1260 days from Revelation.~From 11/12/1997 to 6/29/2016 is 6804 days, and 6804 first occurs in Pi at the end of 1776 digits.',

'556' : '556 is an important number relating to the timeline, and could be seen as a complimentary number to 223, as 556 + 223 = 779. 223 days after 8/29/2019 is 4/8/2020, Passover, a date which is 26262 days after the founding of Israel. 556 days after 4/8/2020 is 10/16/2021, the 289th (17 * 17) day of the year, and the 1st day of the Tzolk\'in cycle.~556 and 223 were the numbers encoded into Isaac Kappy\'s unlocked final message: "July 4th 2019 THE Return of the King Return to THE LIGHT"~223 + 556 + 556 = 1335',

'594' : '594 can represent the middle day of an 1189 day period, as 594 days AFTER the start would bring you to the 595th or middle day of the period. 594 is 297 * 2, and the Bible is made up of 297 + 297 + 1 + 297 + 297 = 1189 chapters.~594 can also represent the 594th day of an 1189 day period, the day before the middle day, the last day/297th day of a 297 day segment.~9/10/2018 + 594 days = 4/26/2020 (middle day)~1/22/2020 + 594 days = 9/7/2021 (middle day)~10/28/2017 + 593 days (594th day) = 6/13/2019',

'595' : '595 represents the middle day of an 1189 day period. The middle chapter of the Bible is Psalm 117. 595 first appears in Pi at the end of 415 digits. 4/15/2014 is the first blood moon of a tetrad, and can be seen as the 595th day of an 1189 day period which starts on 8/29/2012.~9/7/2021 is the 595th day of an 1189 day period~4/26/2020 is the 117th day of the year, and the 595th day of an 1189 day period',

'600' : '600 is 1000 less than 1600, and the first 600 digits of Pi sum to 2667, the number of days from 12/21/2012 to 4/10/2020.',

'603' : '603 first appears in Pi at the end of 265 digits, and the first 603 digits of Pi sum to 2667.~12/21/2012 + 2667 days = 4/10/2020~4/10/2020 - 265 days = 7/20/2019',

'611' : '611 digits of Pi sum to 2701, and 12/21/2012 + 2701 days = 5/14/2020, the 72nd birthday of Israel, a date which is 929 days after 10/28/2017.',

'614' : '614 and 1614 first occur in Pi at position 1614.~10/28/2017 -> 7/4/2019 = 614 days',

'617' : '617 is the 113th prime and first occurs in Pi at the end of 888 digits, directly before the first occurrence of the number 1776 which is 888 + 888. 617 can represent 6/17/2018 which is the start of the 62 week segment of the 70 weeks of Daniel.~4/4/2020 -> 12/12/2021 = 617 days',

'625' : '625 is a very special number relating to the timeline, and has its second occurrence in Pi directly next to 189, as "625189" appears at the end of 1717 digits. 1375 is 40 + 1335, and 1375 squared is "1890625".~The reason 625 is so special is because the first 625 digits of Pi sum to 2772, and 12/21/2012 + 2772 days = 7/24/2020, the completion of the 1150 days from Daniel. Then, 7/24/2020 + 189 days = 1/29/2021, the completion of an important 1189 day period.',

'627' : '627 has its second occurrence in Pi in a very special location: "627 232 7917 8608" ... There are 627 days from 10/28/2017, the start of an important 1189 day period, to 7/17/2019, a date which takes place 7917 days after the start of the 7920 days on 11/12/1997.~8/29/2019 -> 5/17/2021 = 627 days',

'629' : '629 can represent 6/29/2016, the 552nd day of a period which starts 12/26/2014.~135 digits of Pi sum to 629',

'666' : '666 is an extremely important Pi key which first occurs in Pi at the end of 2442 digits, to represent how you must wait 2442 days starting 12/21/2012 to arrive at the beginning of the 1260/1290/1335 days on 8/29/2019. Hebrew word H2442 means "wait" and is used in Daniel 12:12 which says "Blessed is he that waiteth, and cometh to the thousand three hundred and five and thirty days."~Two well known numbers that are used in Revelation are 144000 and 666... The first 144 digits of Pi sum to 666 ... There is another aspect to 666 which makes it an exceptionally special number. The first 666 digits of Pi sum to 2961, and 2961 days after 12/21/2012 is 1/29/2021, the end of a very important 1189 day period.',

'670' : '670 can represent the number of days from 7/17/2019 to 5/17/2021.~145 (up to 146) digits of Pi sum to 670',

'691' : '691 is an extremely important number relating to the timeline as the 691st prime number is 5189 which first occurs in Pi at the end of 1717 digits. 691 first appears in Pi at the end of 895 digits, and 895 is another very important Pi key. 691 is the 125th prime, and the 135th and 145th primes are also very important to the timeline. The 232nd prime number is 1459 and 232 + 1459 = 1691.~12/26/2014 -> 11/16/2016 = 691 days~7/17/2019 -> 6/7/2021 = 691 days',

'701' : '701 is a significant number as there are 701 digits of Pi before the second occurrence of the number 2019. This could represent how the 71st birthday of Israel takes place in 2019. 354 first appears in Pi at the end of 701 digits',

'710' : '710 is a special number because its cosine is 0.99999999. 710 first occurs in Pi directly next to the first occurrence of 853, and is nearby the first occurrence of 9227 in Pi: "853 710 507 9227"~The second occurrence of 710 in Pi appears at the end of 853 digits, directly next to the first occurrence of 1000.~This is a special code as 853 is the year in which the 1144 years began, and 9227 is the 1144th prime. 1000 represents the end of an age.',

'717' : '717 represents 7/17/2019, the 7918th day of the 7920 days. 7/17/2019 represents the day in which Jesus was crucified, and 7/20/2019 represents the day he rose from the dead 3 days later. Jesus then ministered on Earth for 40 days before ascending. Greek word G4717 means "crucify" and is first used in Matthew 20:19.~189 first occurs in Pi at the end of 1717 digits, and 189 days after 7/17/2019 is a very important date on the timeline.',

'720' : '720 can represent 7/20/2019, the completion of the 7920 days and the start of a 40 day period of time. 720 is 360 * 2.~720 first appears in Pi at the end of 1010 digits, as 1010 can be thought of as the number of Jesus. 7/17/2019 represents the day in which Jesus was crucified, and 7/20/2019 represents the day he rose from the dead 3 days later. Jesus then ministered on Earth for 40 days before ascending.~158 (up to 159) digits of Pi sum to 720',

'723' : '723 can represent 7/23/2020, the final day of sacrifice of an 1150 day period of 2300 sacrifices mentioned in The Book of Daniel. 723 has its second occurrence in Pi 1 digit away from the first occurrence of 7917, which is synchronistic as 7917 represents 7/17/2019, a day symbolic of Jesus\' sacrifice on the cross.',

'724' : '724 can represent 7/24/2020, the completion of the 1150 days/2300 sacrifices mentioned in The Book of Daniel.',

'726' : '726 is a significant number which first occurs in Pi directly next to the first occurrence of 360, while intersecting the first occurrence of the number 260. Greek word G726 is one of five words in the New Testament to have a root value of 989, which represents the end of an age. G415 also has a root value of 989. G726 is first used in Matthew 11:12.~7/26/2020 is the 333rd day of the 1260 days which begin 8/29/2019. There are 333 digits of Pi before the first occurrence of 829 or 8292, and 7/26/2020 takes place 8292 days after 11/12/1997, the start of the 7920 days. Greek word G1112 also has a root value of 989.~4/15/2014 -> 7/26/2020 = 2294 days',

'729' : '729 is a very important number as it is 9 * 9 * 9, and the 729th prime is 5519, which represents how 12/21/2012, the end of the 13th baktun, is the 5519th day of the 7920 days. 729 can also represent 7/29/2020, which is 2777 days after 12/21/2012.',

'761' : '761 is an extremely important number relating to the timeline as there are 761 digits of Pi before the "999999" sequence. 761 days after 8/29/2019 is a very important date. The first 761 digits of Pi sum to 3375, which is 225 * 15 or 15 cubed.~9/10/2018 + 761 days = 10/10/2020',

'763' : '763 is a very special number relating to the timeline as 499 first occurs in Pi at the end of 763 digits and 499 represented in octal is also 763. 13499, the 1600th prime, also occurs at the end of 763 digits of Pi.',

'764' : '764 is a significant number relating to Pi as 999 first occurs in Pi at the end of 764 digits.',

'777' : '777 is an important number relating to the timeline. The number 777 is used only in Genesis 5:31 which says "And all the days of Lamech were seven hundred seventy and seven years: and he died." ... This is because 777 days after 5/31/2017 is another important date, 7/17/2019.~777 first occurs in Pi as four 7\'s "7777" at the end of 1592 digits, which is significant as the first couple digits of Pi are "3.14 1592".~777 can also represent 4/10/2020 which has the long count of: 13.0.7.7.7',

'778' : '778 could be short for 5778 or could represent the date 4/11/2020 which has the long count of: 13.0.7.7.8',

'779' : '779 is a very important number relating to the timeline as 779 days after 8/29/2019 is 10/16/2021 (Day 289), the first day of the Tzolk\'in. 779 first occurs in Pi at the end of 4443 digits in this important location: "517 829 666 454 779"~779 is 223 + 556, and these were the numbers encoded into Isaac Kappy\'s unlocked final message: "July 4th 2019 THE Return of the King Return to THE LIGHT"',

'780' : '780 is 260 * 3 and is a very special number relating to the timeline. It appears in Pi like so: "13499999983 729 780 499"~780 (up to 781) digits of Pi sum to 3501 ... 3501 digits of Pi sum to 16000~11/12/1997 -> 1/1/2000 = 780 days~4/12/2015 (13.0.2.6.2) -> 5/31/2017 = 780 days~5/31/2017 -> 7/20/2019 = 780 days',

'800' : '800 is an important number as it is the root value of Greek work G2962 which means "Lord". 800 first appears in Pi at the end of 1599 digits, and 1599 is another very important Pi code.',

'804' : '804 is a significant number as it first appears in Pi at position 777.~5/31/2017 + 777 days = 7/17/2019~7/17/2019 + 804 days = 9/28/2021',

'828' : '828 can represent 8/28/2019, the middle day of the final week of the 70 weeks of Daniel in which the sacrifice ceases.',

'829' : '829 is the 145th prime, and represents 8/29/2019, the start of 1260/1290/1335 days. Matthew 8:29 contains a code for 8/29/2019 and is the first verse to use Greek word G2540 as 829 first occurs in Pi directly next to the first occurrence of 2540. 829 appears at the end of 336 digits of Pi. The first 336 digits of Pi sum to 1501, and 1501 days before 8/29/2019 is another important date on the timeline.',

'831' : '831 could represent 8/31/2019, the last day of the 70 weeks of Daniel.',

'853' : '853 can represent the year 853 A.D. as the 1144 years spoken of by Lord Pakal started in that year. 853 is the reverse of the important Pi key 358. 710 first occurs in Pi directly next to the first occurrence of 853, and is nearby the first occurrence of 9227 in Pi: "853 710 507 9227"~The second occurrence of 710 in Pi appears at the end of 853 digits, directly next to the first occurrence of 1000.~This is a special code as 853 is the year in which the 1144 years began, and 9227 is the 1144th prime. 1000 represents the end of an age.~853 digits of Pi sum to 3800, and 3800 first appears in Pi at the end of 1599 digits. 3800 + 1599 = 5399, the number used in Revelation 2:10 and the number which has its first two occurrences only 1 digit apart.',

'869' : '869 is the three digit number which takes the longest to have its first occurrence in TWO Pi (2Pi). This means that every other 3 digit number has at least one occurrence in 2Pi before the first occurrence of 869. 869 first occurs in 2Pi at the end of 7918 digits, directly next to the second occurrence of 7200. 869 + 7918 = 8787 which first occurs in 2Pi at the end of 8191 digits. 8191 and 7918 are also very important keys in Pi.',

'879' : '879 is 3 * 293 and is a very important Pi code relating to the timeline. The first 879 digits of Pi sum to 3911, one important Pi key, and the 879th prime is 6829, another very important Pi key.',

'888' : '888 is a very special number relating to Pi and the timeline, and is the value of the word "Jesus" in the New Testament. 888 days before 7/17/2019, the day which represents the crucifixion of Jesus, is 2/9/2017, a very important date on the timeline. 888 first appears in Pi as four 8\'s "8888" in this very special location: "1664 1627 4 8888" ... This is significant as you can subtract 888, 1627, or 1664 days from 7/17/2019 to arrive at special dates on the timeline.~The 888th prime is 6907, and 6907 days after 11/12/1997 is 10/10/2016, a date which is 1010 days from 7/17/2019. 1010 days can also be added to 7/17/2019.~There are 888 digits of Pi before the first occurrence of the number 1776 which is 888 + 888.',

'895' : '895 is an extremely important and blatant Pi code which relates to the timeline. 895 occurs directly next to the number 294 in Pi, and these are the first two numbers to occur directly next to each other while summing to 1189, the number of chapters in the Bible. 895 refers to the date 4/10/2020 (13.0.7.7.7), a date which is 294 days from the end and 895 days from the beginning of an important 1189 day period. This date is the 10th and final day of a period of 10 days mentioned in The Book of Revelation. 4/25/2023 is the completion of the 1335 days and the end of a final 1189 day period, and if you subtract 895 days from that date you will arrive at 11/11/2020.~4/15/2014 -> 9/26/2016 = 895 days',

'896' : '896 can refer to the number of days from 10/28/2017 to 4/11/2020. 896 is represented in octal as 1600.',

'917' : '917 can be short for 7917, or could mean 917 days before 7/17/2019, a date which takes place 7917 days after the start of the 7920 days on 11/12/1997. 917 days before 7/17/2019 is 1/11/2017 which is special as 12/21/2012 -> 1/11/2017 = 1482 days, and the first 333 digits of Pi sum to 1482.~917 first occurs in Pi in a special position: "829 2540 917" ... The first 917 digits of Pi sum to 4083, and 483 days after 7/17/2019 is another significant date, 11/11/2020.',

'918' : '918 first occurs in Pi at position 2222 or at the end of 2221 digits. 918 could be short for 7918. 11/11/1918 was the last day of WWI.~10/5/2017 -> 4/10/2020 = 918 days',

'919' : '919 could represent 9/19 which is usually the 262nd day of the year.~12/21/2012 - 1189 days = 9/19/2009 (Day 262) (7/1/5770 (Day 1 C, 178 E))~4/15/2014 -> 7/17/2019 = 1919 days',

'923' : '923 can represent 9/23/2017, the date of the "Revelation 12 Sign". 923 has interesting occurrences in Pi, as its second occurrence is at position 262, then position 700, then 3701, then 4401 ... Notice that those last two occurrences are 700 positions apart.',

'928' : '928 can represent 9/28/2021.',

'929' : '929 is one of the most important numbers relating to Pi and the timeline, and is the 158th prime. There are 929 chapters in the Old Testament and 260 chapters in the New Testament of the Bible. 929 and 260 are complimentary numbers which form a very important number 1189. The 262nd prime number is 1667, and the 1667th prime number is 14159. Then, 262 + 1667 = 1929.~10/28/2017 -> 5/14/2020 = 929 days~3375 can be seen as 929 + 1223 + 1223',

'951' : '951 is a special number as its representation in octal is 1667, and because 951 first occurs in Pi at the end of 390 digits. 390 first occurs in Pi at the end of 1189 digits, a very important timeline number. 951 is also the reverse of 159, one of the first digits of Pi.',

'967' : '967 first appears in Pi directly next to the second occurrence of Pi key 9227, the 1144th prime. 967 can represent 8/29/2019 -> 4/22/2022 = 967 days',

'968' : '968 first appears in Pi directly next to the first occurrence of Pi key 9227, the 1144th prime. 968 can represent 8/28/2019 -> 4/22/2022 = 968 days',

'979' : '979 is one of the well known first couple digits of Pi ("14159 265 358 979 32 384"), and can represent 8/27/2015, a date which takes place 979 days after 12/21/2012. This date is also 24576 days after 5/14/1948, the founding of Israel.~979 occurs near 384 in Pi. 384 digits of Pi sum to 1688, and 1688 + 979 is 2667, the number of days from 12/21/2012 to 4/10/2020~979 could also represent the date 4/2/2022 (13.0.9.7.9) (1/1/5782)',

'989' : '989 is a very important number which represents the end of an age, as it first occurs in Pi at the end of 1000 digits. The first verse in the original 1611 KJV to have a total of 989 is Genesis 8:3 which says "And *(Heb. at the end of dayes.) in processe of time it came to passe, that Cain brought of the fruite of the ground, an offering vnto the LORD."~989 represented in octal is 1735, another very important number. 1735 + 989 = 2724, which occurs at the end of 480 digits of Pi. 12/21/2012 + 480 days = 4/15/2014, the first blood moon of a special tetrad. This is special as Greek word G415 is one of 5 Greek words to have a root value of 989.~989 can also represent the date 4/22/2022 (13.0.9.8.9)',

'1000' : '1000 is a special number as the 1000th prime number is 7919, one less than 7920. There are 853 digits of Pi before the first occurrence of 1000, and 853 can represent the year 853 A.D. as the 1144 years spoken of by Lord Pakal started in that year. A 7920 day period then begins after the completion of the 1144 years.~12/26/2014 -> 9/21/2017 = 1000 days~10/28/2017 -> 7/24/2020 = 1000 days',

'1003' : '1003 can represent the number of days from 7/26/2020 to 4/25/2023. 1003 is a special number because it first appears in Pi at the end of 12294 digits. This is significant as 7/26/2020 takes place 2294 days after 4/15/2014, an important landmark.~You could also say that 7/26/2020 is the middle day and 1003rd day of a 2005 day period from 10/28/2017 to 4/25/2023.~It\'s also interesting to note that 5189 has its first occurrence in Pi at the end of 1717 digits and second occurrence at the end of 4487 digits.~1003 digits of Pi sum to 4487',

'1005' : '1005 is a very important Pi key which can represent the number of days from 7/24/2020, the completion of the 1150 days, to 4/25/2023, the completion of the 1335 days. 1005 has its first occurrence in Pi in this very special location: "531 910 4848 1005" ... 531 can represent 5/31/2017, the beginning of the 1150 days/2300 sacrifices from The Book of Daniel. 4848 is double 2424, the number of Jesus, who sacrificed himself on the cross.~4/29/2018 -> 1/28/2021 = 1005 days~222 digits of Pi sum to 1005',

'1010' : '1010 can be thought of as the number of Jesus. 7/17/2019 represents the day Jesus was crucified. 7/17/2019 - 1010 days = 10/10/2016, a date which is 6907 (888th prime) days after 11/12/1997. 7/17/2019 + 1010 days = 4/22/2022 (13.0.9.8.9)~7/20/2019 represents the day Jesus rose from the dead 3 days later. 720 first appears in Pi at the end of 1010 digits.~1010 could also represent 12/25/2020 (10/10/5781)',

'1038' : '1038 is 519 * 2, and first appears in Pi directly next to the third occurrence of four 7\'s like so: "7777 1038"',

'1040' : '1040 is 260 * 4 and is an interesting number as it is represented in hexadecimal as 410 and in octal as 2020. This number could be a good code for representing the important date 4/10/2020.~9/13/2016 -> 7/20/2019 = 1040 days',

'1112' : '1112 can represent 11/12/1997, the completion of the 1144 years and the start of 7920 days. Greek word G1112 is one of five word in the New Testament to have a root value of 989, which indicates the end of an age. The number of Jesus, 2424, first occurs in Pi at the end of 1111 digits or at position 1112. 1112 is 278 * 4 or 556 * 2.~4/8/2020 -> 4/25/2023 = 1112 days',

'1116' : '1116 could be representative of a sacrifice. Revelation mentions a period of 150 days, and 150 first appears in Pi at the end of 1116 digits. 1116 could also represent the date 11/16/2016.~7/23/2020 is the last day of sacrifice of the 1150 days and has the Coptic date: 11/16/1736',

'1119' : '1119 first occurs in Pi directly next to the number 8766, and 8766 represents 24 years or 365 * 24 days plus 6 days for leap years.~4/1/2020 -> 4/25/2023 = 1119 days',

'1125' : '1125 is an interesting number as the second occurrence of 829 occurs at the end of 1125 digits. 1125 * 3 = 3375. Greek word G2540 is used for the second time in the Bible in Matthew 11:25.~1125 could represent the date 11/25/2015 or 11/25/2017',

'1129' : '1129 is the 189th prime number and 189 first appears in Pi at the end of 1717 digits. 1129 first occurs in Pi at this important position: "517 829 666 454 779 17450 1129"~51 digits of Pi sum to 249 ... 249 digits of Pi sum to 1129 ... 1129 digits of Pi sum to 5073~1129 could represent the date 11/29/2018 or 11/29/2020~11/29/2020 is the 1129th day of a period in which the first day is 10/28/2017.',

'1139' : '1139 is significant because it first appears in Pi at the end of 1188 digits, or at position 1189.',

'1144' : '1144 is a very important number which can represent the 1144 year period which is completed on 11/12/1997. The 1144th prime is 9227.~Refer to ..710 / ..853 / ..1000 for more information',

'1150' : '1150 is a very important number which can represent the 1150 days/2300 sacrifices mentioned in The Book of Daniel.~5/31/2017 -> 7/24/2020 = 1150 days~Refer to ..531 / ..1005 for more information',

'1170' : '1170 is an interesting number as its representation in octal is 2222. 255 first appears in Pi at the end of 1170 digits. The first 1170 digits of Pi sum to 5287~11/12/1997 + 5287 days = 5/4/2012~8/29/2019 + 5287 days = 2/18/2034 (13.1.1.8.9)',

'1188' : '1188 is 1189 - 1, or 297 + 297 + 297 + 297. It first appears in Pi in this interesting location: "11881 710 1000" ... 1188 is also 2.2 * 540 or 22 * 54.',

'1189' : '1189 is an extremely important number relating to Pi and the timeline, as there are 1189 chapters in the Bible. The sum of the divisors of 1189 is 1260. 1189 days can be broken up into 929 + 260 days, as there are 929 chapters in the Old Testament and 260 chapters in the New Testament. 1189 can also be broken up into 297 + 297 + 1 + 297 + 297 days. There are many important 1189 day periods which make up the timeline.~9/19/2009 -> 12/21/2012 = 1189 days~8/29/2012 -> 12/1/2015 = 1189 days~9/23/2017 -> 12/25/2020 = 1189 days~10/28/2017 -> 1/29/2021 = 1189 days~9/10/2018 -> 12/12/2021 = 1189 days~1/22/2020 -> 4/25/2023 = 1189 days',

'1221' : '1221 is a special Pi key which has its second occurrence in Pi directly next to the second occurrence of 5519, which is synchronistic as 12/21/2012 is the 5519th day of the 7920 days. 1221 * 2 is 2442, and 2442 days after 12/21/2012 is 8/29/2019, the start of the 1260/1290/1335 days.~8/29/2019 -> 1/1/2023 = 1221 days',

'1223' : '1223 is the 200th prime number, and 929 + 1223 + 1223 = 3375.~12/26/2014 + 1223 days = 5/2/2018',

'1225' : '1225 is a special number as Christmas is 12/25. The 1225th prime is 9931 which first appears in Pi at the end of 22222 digits. 9931 is also the reverse of 1399, which is the 222nd prime number. 1225 can represent the date 12/25/2020.',

'1226' : '1226 can represent the date 12/26/2014. 1226 first appears in Pi at the end of 966 digits, and 966 first appears in Pi at the end of 1332 digits.~12/26/2014 - 966 days = 5/4/2012~4/30/2018 + 1226 days = 9/7/2021~9/21/2017 -> 1/29/2021 = 1226 days',

'1257' : '1257 is an interesting number as it first occurs in Pi at position 4060, then position 7700, then 32999, then 34888. 1257 is the number of days from 9/1/2019, the completion of the 70 weeks of Daniel, to 2/9/2023, the completion of the 1260 days.~4/15/2014 -> 9/23/2017 = 1257 days',

'1260' : '1260 is a very important number relating to the timeline as an important 1260 day period starts on 8/29/2019. Matthew 8:29 is Verse #23375 and contains code relating to the 1260 days. Interestingly, the 1260th prime is 10271 which first appears in Pi like so: "3375 10271"~5/31/2017 -> 11/11/2020 = 1260 days',

'1290' : '1290 is a very important number relating to the timeline as an important 1290 day period starts on 8/29/2019.',

'1300' : '1300 is 260 * 5, and appears in Pi like so: "1226 8066 1300 1927 8766 1119" ... It has its second occurrence in Pi directly next to the first occurrence of 5005.~1/1/2017 -> 7/24/2020 = 1300 days~7/20/2019 -> 2/9/2023 = 1300 days~9/7/2021 -> 3/30/2025 = 1300 days',

'1312' : '1312 is a significant number as 289 (17 * 17) first occurs in Pi at the end of 1312 digits. The first occurrence of 1312 in Pi intersects an occurrence of 2961 like so: "2961312"',

'1319' : '1319 is a special number as 294 digits of Pi sum to 1319 and 1319 digits of Pi sum to 5957, an important Pi code. 10/28/2017 + 5957 days = 2/18/2034 (13.1.1.8.9) ... Greek word G726 is used for the second time in the Bible in Matthew 13:19. 1319 is similar to the number 31319 which is the 3375th prime.',

'1327' : '1327 is a very important Pi key which first occurs in Pi in a very important area: "7029 1327 6561". 6561 - 1327 = 5234 which occurs sandwiched between two very important numbers: "1003 5234 3777"~1620 first occurs in Pi at the end of 1327 digits, and has its next occurrence at the end of 3981 digits, which is 1327 * 3. 1620 + 1327 is 2947 which occurs directly next to an occurrence of 2654 in Pi. 1327 * 2 = 2654, and very important Pi key 2265 first occurs in Pi at the end of 2654 digits. 2265 + 2654 = 4919 which first occurs in Pi at position 1620.~727 represented in octal is 1327~11/12/1997 -> 7/1/2001 = 1327 days~12/1/2015 -> 7/20/2019 = 1327 days',

'1332' : '1332 is 666 + 666 and is the number of days from the completion of the 70 weeks of Daniel on 9/1/2019 to the completion of the 1335 days on 4/25/2023.',

'1335' : '1335 is a very important number relating to the timeline as an important 1335 day period starts on 8/29/2019.',

'1375' : '1375 can be seen as 40 + 1335, and is an interesting number as 1375 squared is 1890625. 625189 occurs at the end of 1717 digits of Pi. The second occurrence of 1375 in Pi appears directly next to the first occurrence of 2239, the 333rd prime.~12/21/2012 -> 9/26/2016 = 1375 days~7/20/2019 -> 4/25/2023 = 1375 days',

'1399' : '1399 is an extremely important number relating to Pi and the timeline as 9/11/2001 takes place 1399 days after the start of the 7920 days on 11/12/1997. 1399 is the 222nd prime number, and the reverse of 1399 is 9931, the 1225th prime, which first occurs in Pi at the end of 22222 digits.~1399 first appears in Pi like so: "16566 1399 1999" ...  Notice that 1656 is the reverse of 6561. 6561 is 9 * 9 * 9 * 9, and 6561 days after 9/11/2001 is 8/29/2019, the start of the 1260 days from Revelation. Important Pi key 9227 has its second occurrence in Pi at the end of 1399 digits. This is synchronistic as 9227 is the 1144th prime number, and 11/12/1997 marks the completion of the 1144 years. 1399 days after that date is 9/11/2001.~The date 12/25 is always 1399 days away from 2/25 three years earlier.~11/12/1997 -> 9/11/2001 = 1399 days~9/26/2016 -> 7/26/2020 = 1399 days',

'1425' : '1425 is noteworthy as the 1425th prime number is 11897 and 11897 is the first prime to contain the number 1189. 4/25/2023 is the completion of a final 1189 day period. 11/12/1425 is also the start of the 12th 52 year cycle of the 1144 years.',

'1427' : '1427 is an interesting number as it is the 225th prime, and there are 2665 digits of Pi before the first occurrence of 1427. This could be representative of how 4/8/2020 is the 225th day of the Tzolk\'in and takes place 2665 days after 12/21/2012.',

'1444' : '1444 is an interesting number as it first occurs in Pi at the end of 3478 digits. 3478 is the number of Israel. The sum of the divisors of 1444 equals 2667 which is another very important number of the timeline.',

'1459' : '1459 is a very important number relating to Pi and the timeline. It is the first 5 digits of Pi except the 1 in the middle. 1459 is the 232nd prime, and 1459 + 232 = 1691. 691/1691 are very important timeline codes. The 1459th prime is 12203 which resembles 1223, the 200th prime. Also, the first 1459 digits of Pi sum to 6562. You could think of 8/29/2019 as being the 6562nd day of a period which starts on 9/11/2001, or 6562 days after 9/10/2001, the last day of coptic year 1717.~1459 first appears in Pi at the end of 3240 digits, and 3240 first appears in Pi at the end of 13333 digits~14159 - 1459 = 12700, and there are 12700 digits of Pi before the first occurrence of 1112 which represents 11/12/1997, the start of the 7920 days. Matthew 11:12 has a verse total of 12700. 12700 is also 2540 * 5.~11/12/1997 + 1459 days = 11/10/2001 (1 (1, Imix\'))~4/13/2016 -> 4/11/2020 = 1459 days',

'1592' : '1592 is a special number because it is one of the first few digits of Pi, and because the first occurrence of 7777 in Pi appears at the end of 1592 digits.~7/17/2019 -> 11/25/2023 (13.0.11.1.11) = 1592 days',

'1598' : '1598 first appears in Pi directly next to the first occurrence of 1362. 12/21/2012 + 1362 days = 9/13/2016 (222 (1, Ik\')), and 9/13/2016 + 1598 days = 1/28/2021, the final day/1189th day of an important 1189 day period. 1362 + 1598 = 2960, 1 less than important Pi key 2961.',

'1599' : '1599 is a very important number which relates to Pi and the timeline. 5280 first occurs in Pi directly next to the first occurrence of 1735. 5280 + 1735 = 7015, and 1599 first appears in Pi at the end of 7015 digits. 280 + 1599 = 1879, the 289th prime. 1599 + 1735 = 3334 which is 1667 * 2.~1599 + 2708 + 2708 = 7015~Greek word G2962 "Lord" has a root value of 800, and 800 first appears in Pi at the end of 1599 digits. If you subtract 1599 days from the first day of the Tzolk\'in, you arrive at the 222nd day.~11/25/2015 -> 4/11/2020 = 1599 days~5/31/2017 -> 10/16/2021 = 1599 days~1/29/2021 - 1599 days = 9/13/2016 (222 (1, Ik\'))~1/28/2021 + 1599 days = 6/15/2025',
}

#	'' : '',

#-----------------------------------------------------------------------
# Take input from user and decide whether they are entering a date, a number, or a text message

exit_flag = False
extra_search = False
extra_search_count = 2
last_command = 'math'		# (Current available commands) = measure_date, add_date, subtract_date, lone_date_group, number, math, library_search, pi_search, gematria, extra_search, paste_gematria
last_num = '2424'

a = []
b = []

def mainLoop():

	global exit_flag, extra_search, last_command, last_num

	while True:

		try:

			newlines = '\n\n'

			if extra_search:
				extra_search = False
				newlines = '\n'

			user_input = raw_input(newlines + 'Input: ').strip()			# No trailing or leading spaces

			if user_input.lower() == 'exit':	# Exit program
				exit_flag = True
				exit()

			num_with_leading_zeros = user_input	# String

			try_eval = True
			eval_result = ''
			eval_user_input = ''

			try:
				eval_user_input = user_input.replace('"', '').replace("'", '')	# Remove double and single quotes
				eval_result = eval(eval_user_input)
			except:
				try_eval = False

			pi_search = 1

			try:
				pi_search = int(user_input.split('//', 1)[1])
				num_with_leading_zeros = user_input.split('//', 1)[1]
			except:
				pi_search = 0

			library_search = 1

			try:
				library_search = user_input.split('..', 1)[1]
				if not library_search in number_library:
					library_search = 0
			except:
				library_search = 0

			contains_arrow = False
			contains_plus = False
			contains_minus = False
			date_group = False
			lone_date_group = False
			lone_number = False
			separator = ''

			if len(user_input.split(' ')) == 3 and user_input.replace(' ', '').isdigit():
				lone_date_group = True

			if user_input.isdigit():
				lone_number = True

			if '+' in user_input:
				contains_plus = True
				separator = '+'
			if '-' in user_input and not '->' in user_input:
				contains_minus = True
				separator = '-'
			if '->' in user_input:
				contains_arrow = True
				separator = '->'

			if contains_plus or contains_minus:
				left_side = user_input.split(separator, 1)[0].strip()
				right_side = user_input.split(separator, 1)[1].strip()

				if len(left_side.split(' ')) == 3 and left_side.replace(' ', '').isdigit() and right_side.isdigit():
						# There are three groups of numbers on left side, and the right side contains just a number
						date_group = True
				if left_side.lower() == 'a' or left_side.lower() == 'b' and right_side.isdigit():
						date_group = True

			if contains_arrow:
				left_side = user_input.split(separator, 1)[0].strip()
				right_side = user_input.split(separator, 1)[1].strip()

				left_group = False
				right_group = False

				if len(left_side.split(' ')) == 3 and left_side.replace(' ', '').isdigit():		# There are three groups of numbers on left side
						left_group = True
				if len(right_side.split(' ')) == 3 and right_side.replace(' ', '').isdigit():	# There are three groups of numbers on right side
						right_group = True

				if left_side.lower() == 'a' or left_side.lower() == 'b':
						left_group = True
				if right_side.lower() == 'a' or right_side.lower() == 'b':
						right_group = True

				if left_group and right_group:
						date_group = True

			if contains_arrow and date_group:			# We are measuring the distance between two dates
				last_command = 'measure_date'
				first_date = user_input.split('->', 1)[0].strip().lower()
				second_date = user_input.split('->', 1)[1].strip().lower()

				start_year, start_month, start_day = None, None, None
				end_year, end_month, end_day = None, None, None

				if first_date == 'a':
						start_year, start_month, start_day = a[0], a[1], a[2]
				elif first_date == 'b':
						start_year, start_month, start_day = b[0], b[1], b[2]
				else:
						start_year, start_month, start_day = split_up_date(first_date)

				if second_date == 'b':
						end_year, end_month, end_day = b[0], b[1], b[2]
				elif second_date == 'a':
						end_year, end_month, end_day = a[0], a[1], a[2]
				else:
						end_year, end_month, end_day = split_up_date(second_date)

				a = [start_year, start_month, start_day]
				b = [end_year, end_month, end_day]

				start = dt.datetime(start_year, start_month, start_day, 0, 0, 0)
				end = dt.datetime(end_year, end_month, end_day, 0, 0, 0)
				delta = end - start

				result = str(delta.days)

				if delta.days < 0:
						result = str(-delta.days)

				start_date_nice = str(start_month) + '/' + str(start_day) + '/' + str(start_year)
				end_date_nice = str(end_month) + '/' + str(end_day) + '/' + str(end_year)

				info_available_1 = False
				info_available_2 = False

				if start_date_nice.replace('/', ' ') in number_library:
					info_available_1 = True
				if end_date_nice.replace('/', ' ') in number_library:
					info_available_2 = True

				print_date_information(start_year, start_month, start_day, end_year, end_month, end_day, info_available_1, info_available_2)

				result_string = '\n\n' + start_date_nice + ' -> ' + end_date_nice + ' = ' + str(result) + ' days'

				print(result_string)

			elif contains_plus and date_group:			# We are adding a certain number of days to a date
				last_command = 'add_date'
				first_date = user_input.split('+', 1)[0].strip().lower()
				the_days = int(user_input.split('+', 1)[1].strip())

				start_year, start_month, start_day = None, None, None

				if first_date == 'a':
						start_year, start_month, start_day = a[0], a[1], a[2]
				elif first_date == 'b':
						start_year, start_month, start_day = b[0], b[1], b[2]
				else:
						start_year, start_month, start_day = split_up_date(first_date)

				start = dt.datetime(start_year, start_month, start_day, 0, 0, 0)

				r_date = start + dt.timedelta(the_days)
				end_year = r_date.year
				end_month = r_date.month
				end_day = r_date.day

				a = [start_year, start_month, start_day]
				b = [end_year, end_month, end_day]

				start_date_nice = str(start_month) + '/' + str(start_day) + '/' + str(start_year)
				end_date_nice = str(end_month) + '/' + str(end_day) + '/' + str(end_year)
				result_string = '\n\n' + start_date_nice + ' + ' + str(the_days) + ' days = ' + end_date_nice

				info_available_1 = False
				info_available_2 = False

				if start_date_nice.replace('/', ' ') in number_library:
					info_available_1 = True
				if end_date_nice.replace('/', ' ') in number_library:
					info_available_2 = True

				print_date_information(start_year, start_month, start_day, end_year, end_month, end_day, info_available_1, info_available_2)

				print(result_string)

			elif contains_minus and date_group:			# We are subtracting a certain number of days from a date
				last_command = 'subtract_date'
				first_date = user_input.split('-', 1)[0].strip().lower()
				the_days = int(user_input.split('-', 1)[1].strip())

				start_year, start_month, start_day = None, None, None

				if first_date == 'a':
						start_year, start_month, start_day = a[0], a[1], a[2]
				elif first_date == 'b':
						start_year, start_month, start_day = b[0], b[1], b[2]
				else:
						start_year, start_month, start_day = split_up_date(first_date)

				start = dt.datetime(start_year, start_month, start_day, 0, 0, 0)

				r_date = start - dt.timedelta(the_days)
				end_year = r_date.year
				end_month = r_date.month
				end_day = r_date.day

				a = [start_year, start_month, start_day]
				b = [end_year, end_month, end_day]

				start_date_nice = str(start_month) + '/' + str(start_day) + '/' + str(start_year)
				end_date_nice = str(end_month) + '/' + str(end_day) + '/' + str(end_year)
				result_string = '\n\n' + start_date_nice + ' - ' + str(the_days) + ' days = ' + end_date_nice

				info_available_1 = False
				info_available_2 = False

				if start_date_nice.replace('/', ' ') in number_library:
					info_available_1 = True
				if end_date_nice.replace('/', ' ') in number_library:
					info_available_2 = True

				print_date_information(start_year, start_month, start_day, end_year, end_month, end_day, info_available_1, info_available_2)

				print(result_string)

			elif lone_date_group:			# The user_input is simply a date group, so we will display its information
				last_command = 'lone_date_group'
				year, month, day = split_up_date(user_input)

				info_available_1 = False

				if user_input in number_library:
					info_available_1 = True

				print_date_information(year, month, day, None, None, None, info_available_1, None)

			#-----------------------------------------------------------------------
			# Analyze number

			elif lone_number:				# The user_input is an integer for us to display its properties
				last_command = 'number'
				num = int(user_input)
				last_num = user_input

				factorization = prime_factors(num)
				divisors = list(divisorGenerator(num))
				sum_of_divisors = sum(divisors)
				prime_num, nth_prime, previous_prime, next_prime = prime_info(num)
				prev_int = str(num - 1)
				next_int = str(num + 1)
				binary = bin(num)[2:]
				octal = oct(num).lstrip('0')
				hexadecimal = hex(num)[2:]
				duodecimal = base10toN(num, 12).replace(':', 'A').lower()
				square = num * num
				square_root = num ** (1/2.0)
				square_root = ('%f' % square_root).rstrip('0').rstrip('.')
				cube_root = is_perfect_cube(num)
				isFib = isFibonacci(num)
				isFac = isFactorial(num)
				isReg = isRegular(num, factorization)
				isPerf = isPerfect(num, divisors)
				nat_log = math.log(num)
				dec_log = math.log10(num)
				sine = math.sin(num)
				cosine = math.cos(num)
				tangent = math.tan(num)

				print('\n')

				first_part = ''
				len1 = 20
				len2 = 19

				if len(prev_int) % 2 != 0:  # Is not even length
						len1 = 19

				first_part = (((len1 - len(prev_int)) / 2) * ' ')
				next_part = (((len2 - len(next_int)) / 2) * ' ')

				line = first_part + prev_int + next_part + str(num) + next_part + next_int

				if user_input in number_library:
					line += '       (Info Available!)\n'
				else:
					line += '\n'

				print(line)

				print('Factorization:     ' + str(factorization).replace('[', '').replace(']', '').replace(', ', ' * '))
				print('Divisors:          ' + str(divisors).replace('[', '').replace(']', ''))
				print('Count of divisors: ' + str(len(divisors)))
				print('Sum of divisors:   ' + str(sum_of_divisors) + '\n')

				prime_1 = 'Previous prime:    ' + str(previous_prime)
				prime_2 = 'Next prime:        ' + str(next_prime)
				prime_3 = ''
				prime_4 = ''

				if prime_num:
						prime_3 = 'Prime?: YES, prime #' + str(prime_num) + ''
				else:
						prime_3 = 'Prime?: NO'

				prime_s = 'Prime #' + str(num) + ' is:'
				prime_s += ' ' * (19 - len(prime_s))
				prime_4 = prime_s + str(nth_prime)

				prime_line1 = format(prime_1, prime_3)
				prime_line2 = format(prime_2, prime_4)

				print(prime_line1)
				print(prime_line2 + '\n')

				bases_1 = 'Binary:            ' + binary
				bases_2 = 'Octal:             ' + octal
				bases_3 = 'Duodecimal:        ' + duodecimal
				bases_4 = 'Hexadecimal:       ' + hexadecimal

				bases_line1 = format(bases_1, bases_3)
				bases_line2 = format(bases_2, bases_4)

				print(bases_line1)
				print(bases_line2 + '\n')

				if isFib or isFac or isReg or isPerf:

						if isFib:
							print('Is a Fibonacci number!')
						if isFac:
							print('Is a Factorial!')
						if isReg:
							print('Is a Regular number!')
						if isPerf:
							print('Is a Perfect number!')

						print('')

				square_1 = 'Square:            ' + str(square)
				square_r = 'Square root:       ' + str(square_root)

				info1 = 'Natural logarithm: ' + str(nat_log)
				info2 = 'Decimal logarithm: ' + str(dec_log)
				info3 = 'Sine:              ' + str(sine)
				info4 = 'Cosine:            ' + str(cosine)
				info5 = 'Tangent:           ' + str(tangent)

				info_line1 = format(square_1, info1)
				info_line2 = format(square_r, info2)
				info_line3 = ''

				if cube_root:
						cube_r = 'Cube root:         ' + str(cube_root)
						info_line3 = format(cube_r, info3)
				else:
						info_line3 = format('', info3)

				info_line4 = format('', info4)
				info_line5 = format('', info5)

				print(info_line1)
				print(info_line2)
				print(info_line3)
				print(info_line4)
				print(info_line5)

				pi_info = search_in_pi(num_with_leading_zeros, 1)

				print('\n' + pi_info)

				pi_sum = digit_sum_pi(num)

				if pi_sum != '':
						if (not pi_info.endswith('\n\n')) and (not pi_info.endswith('^')):			# Keep formatting consistent
							print('\n' + pi_sum)
						else:
							print(pi_sum)

			#-----------------------------------------------------------------------
			# Simple math tool

			elif try_eval:
				last_command = 'math'
				print('\n\n' + str(eval_result))

			#-----------------------------------------------------------------------
			# Library search

			elif library_search:
				last_command = 'library_search'

				console_width = get_terminal_size()[0]

				entry = number_library[library_search]
				paragraphs = entry.split('~')
				complete = ''

				for paragraph in paragraphs:
					lines = textwrap.wrap(paragraph, console_width)
					for line in lines:
						complete += line + '\n'
					complete += '\n'

				while complete.endswith('\n'): complete = complete[:-1]

				print('\n\n' + complete)

			#-----------------------------------------------------------------------
			# Pi search tool

			elif pi_search:
				last_command = 'pi_search'
				find_multiple_pi(num_with_leading_zeros)

			#-----------------------------------------------------------------------
			# Analyze gematria

			else:
				if user_input == '' or eval_user_input == '':		# The second_function sends a newline and this function may receive it
					continue

				last_command = 'gematria'

				wordnum, letternum, infostring, totalEO, totalFR, totalRO, totalRFR, all_total, EOletters, wordvals, letters = Gematria(user_input)

				if wordnum == None:
					print('\n\nText could not be decoded')
					continue

				complete = Gematria_print(wordnum, letternum, infostring, totalEO, totalFR, totalRO, totalRFR, all_total, EOletters, wordvals, letters)
				print('\n\n' + complete)

		except SystemExit:
			exit()

		except:
			pass

		"""
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print(e)
			print(exc_type, exc_tb.tb_lineno)
			pass
		"""

keyboard = Controller()
thread = None

def second_function(key):
	global extra_search, extra_search_count, last_command

	if exit_flag == True:
		return False

	if key == Key.shift_r:
		# Find next occurrence of last searched number in Pi

		if last_command != 'extra_search':
			if last_command == 'number':
				extra_search_count = 2
			else:
				extra_search_count = 1

		last_command = 'extra_search'
		extra_search = True

		pi_info = search_in_pi(last_num, extra_search_count)

		if 'This number does not' in pi_info and 'What occurs at' not in pi_info:
			pi_info += '\n'

		extra_search_count += 1
		sys.stdout.write('\n\n\n' + pi_info)				# No newline at end

		keyboard.press(key.enter)							# Returns to main loop
		keyboard.release(key.enter)

	if key == Key.ctrl_r:
		# Get clipboard contents and check Gematria

		last_command = 'paste_gematria'
		wordnum, letternum, infostring, totalEO, totalFR, totalRO, totalRFR, all_total, EOletters, wordvals, letters = Gematria(clipboard.paste().encode('utf-8'))		# Encode command is needed

		if wordnum == None:
			sys.stdout.write('\n\n\nText could not be decoded')
		else:
			complete = Gematria_print(wordnum, letternum, infostring, totalEO, totalFR, totalRO, totalRFR, all_total, EOletters, wordvals, letters)
			sys.stdout.write('\n\n\n' + complete)

		keyboard.press(key.enter)							# Returns to main loop
		keyboard.release(key.enter)

thread = Thread(target=mainLoop)
thread.start()

with Listener(on_release=second_function) as listener:
	listener.join()
