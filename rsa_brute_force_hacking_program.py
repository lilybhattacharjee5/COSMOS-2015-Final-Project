# RSA BRUTE FORCE HACKING PROGRAM (SIMULATION)

# The libraries that will be used in the program are imported along with all of their functions.
import math, random, time
# Right after the program begins, the computer begins counting the number of seconds it takes to execute the program.
start = time.time()
# These values are placeholders for the values present in the public key. The public key is known to everyone, including the hacker.
j = 3
n = 2840407
# The following is the format of the public key in the program. This is optional, but makes values easier to locate.
public_key_of_hacked_person = ['Amy',(j,n)]
print "Amy - a user of RSA - is being hacked. Her public key is (" + str(j) + "," + str(n) + ").\n"
# This is the set to which factors of n will be pushed. Generally, n would take a long time to factor, but in this simulation, small
# primes are used to streamline the program and reduce runtime to a manageable length of time.
factors_of_n = []
# The following algorithm, based on the findfactors() function in the previous RSA simulation, helps find the prime factors of n
# quickly by splitting n from its square downwards and entering the first prime and its complement at the same time instead of
# finding both individually.
for i in range(2,int(math.ceil(math.sqrt(n)))):
    if n % i == 0:
        factors_of_n.append(i)
        factors_of_n.append(n/i)
# variables encompassing the two large primes
p = factors_of_n[0]
q = factors_of_n[1]
# The factors are presented in an output to the user.
print "The second element - n - from the public key has been factored into the following: " + str(p) + " and " + str(q) + ".\n"
# The value of d from the RSA simulation is determined using the following formulas.
tot_result = (p - 1) * (q - 1)
r = 1
while float(tot_result*r+1) % float(j) != 0:
    r += 1
d = int(float(tot_result*r+1)/float(j))
# The private key can now be assembled after knowing the values of d and n which was already in the public key.
private_key_of_hacked_person = (d,n)
# The private key is presented in an output to the user.
print "Amy's private key is (" + str(d) + ", " + str(n) + ").\n"
# The secret message being sent from Bob to Amy is 42. However, even though the message is encrypted when sent, the hacker has
# already infiltrated Amy's private key, so he can decrypt the message as well.
secret_message = 42
encrypted_message = pow(secret_message,j) % n
print "The hacker sees " + str(encrypted_message) + " being sent from Bob to Amy. Using Amy's private key, he can decrypt the message.\n"
print "Decrypting...\n"
decrypted_message = pow(encrypted_message,d) % n
print "In this way, the decrypted message is " + str(decrypted_message) + ". Check inside the code in the variable secret_message to make sure!\n"
# After finishing the program, the computer stops counting seconds of runtime and outputs the amount of time it took to hack the
# RSA private key to the user.
end = time.time()
print "The program has taken " + str(end - start) + " seconds to run."
