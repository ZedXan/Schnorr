#!/usr/bin/python
# -*- coding: utf-8 -*-

import bint as lib
import sys
import random


def miller_rabin_pass(a, s, d, n):
	a_to_power = pow(a, d, n)

	if a_to_power == 1:
		return True

	for i in xrange(s - 1):
		if a_to_power == n - 1:
			return True
		a_to_power = (a_to_power * a_to_power) % n

	return a_to_power == n - 1


def miller_rabin(n):
	"""Тест Миллера-Рабина на простоту числа

	"""
	d = n - 1
	s = 0

	while d % 2 == 0:
		d >>= 1
		s += 1

	for repeat in xrange(20):
		a = 0

		while a == 0:
			a = random.randrange(n)
		if not miller_rabin_pass(a, s, d, n):
			return False

	return True


def prime_test(num):
	if not miller_rabin(num):
		raise ValueError("Выбранное число не является простым.")


def xgcd(a, b):
	"""Расширенный алгоритм Евклида

	"""
	if a == lib.bint(0):
		return 0, 1, b

	if b == lib.bint(0):
		return 1, 0, a

	px = lib.bint(0)
	ppx = lib.bint(1)
	py = lib.bint(1)
	ppy = lib.bint(0)

	while b > lib.bint(0):
		q = a / b
		a, b = b, a % b
		x = ppx - q * px
		y = ppy - q * py
		ppx, px = px, x
		ppy, py = py, y

	return ppx, ppy, a


def inverse(a, p):
	x, y, g = xgcd(a, p)

	return (x % p + p) % p


def gen_keys():
	"""Генерирует ключи

	"""
	f = open("p.txt")

	p = int(f.read())

	f.close()

	f = open("q.txt")

	q = int(f.read())

	f.close()

	f = open("g.txt")

	g = int(f.read())

	f.close()

	prime_test(p)
	prime_test(q)

	w = random.randint(2, q - 1)

	r = random.randint(2, q - 1)

	p = lib.bint(str(p))
	q = lib.bint(str(q))
	g = lib.bint(str(g))
	w = lib.bint(str(w))
	r = lib.bint(str(r))

	inv_g = inverse(g, p)

	y = p.powmod(inv_g, w, p)

	x = p.powmod(g, r, p)

	print "\nКлючи сгенерированы:\n"

	print "x = ", x, "отсылается Виктору\n"

	return p, q, g, w, r, y, x


def schnorr(p, q, g, w, r, y, x):
	e = random.randint(0, pow(2, 20) - 1)

	e = lib.bint(str(e))

	print "e = ", e, "отсылается Пегги\n"

	s = (r + w * e) % q

	print "s = ", s, "отсылается Виктору\n"

	m1 = p.powmod(g, s, p)
	m2 = p.powmod(y, e, p)

	m = (m1 * m2) % p

	if m == x:
		print "Виктор удостоверился в подлинности x = ", m, "\n"
	else:
		print "Подлинность не установлена\n"


if __name__ == "__main__":
	p, q, g, w, r, y, x = gen_keys()

	schnorr(p, q, g, w, r, y, x)
