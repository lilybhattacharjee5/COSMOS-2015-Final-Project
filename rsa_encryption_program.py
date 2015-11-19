# RSA ENCRYPTION/DECRYPTION PROGRAM (SIMULATION)

# The two libraries of functions that will be used in the program are activated.
import math, random
# The function of the status variable is to determine whether or not the user would like to continue sending messages. If the user
# inputs "no" (not case-sensitive) after the first round, the program exits and must be restarted to continue.
status = True

# This is the body loop of the program. While status is True, the program runs, so the entire program is present inside the loop.
while status:

    # This statement is structured so that is positioned before the printed public keys.
    print "Your Contacts:"

    # DEFINITIONS
    # This is the set of public keys that is generated each time after the program restarts. The sender can see the public keys.
    public_keys = []
    # This is the set of private keys that is also generated after each restart. The sender does not know the private keys. The
    # private keys are used for decrypting sent messages.
    private_keys = []
    # This set includes possible recipients of the sent message.
    people = ["Amy","Bob","Cathy"]
    # This empty set will later be used to contain factors of various numbers (including generated primes) throughout the program.
    factors_of_number = []
    # The generation of public keys and private keys will only run as many times as the number of people in order to give each person
    # his or her unique keys.
    people_index = 0
    # In a real RSA implementation, there would be no compiled set of prime numbers. However, this set includes all primes between
    # 1 and 1000 (at the moment) to make it easier to obtain semi-large primes.
    set_of_primes = []
    # This is the editable high limit of each generated prime.
    prime_limit = 1000
    # Because Fermat's Little Theorem has exceptions known as Fermat Liars and Carmichael numbers during prime generation, the list
    # of possible primes (from the implementation of FlT) is cross-checked with brute force factorization to make sure that numbers
    # generated are actually prime. Having a composite number in the list could potentially yield incorrect results in modular
    # functions.
    possible_prime_list = []

    # FUNCTION
    # This function will generate the factors of any number upon which the function is performed.
    def findfactors(number):
        for i in range(2,number+1):
            if number % i == 0:
                factors_of_number.append(i)

    # PRIME GENERATION
    # This loop uses a prime detection method inspired by Fermat's Little Theorem to find 'possible' primes. As stated before, FlT
    # has semi-rare exceptions (e.g. 561, which is a composite as it can be factorized to 3 * 17 * 11), so numbers that satisfy the
    # following conditions will be pushed to the list of 'possible' primes instead of immediately going to the list of true primes.
    for i in range(2,prime_limit):
        prime_base = random.randrange(1,i)
        if (prime_base ** (i - 1)) % i == 1:
            possible_prime_list.append(i)
    # This brute force loop checks the FlT generated list by using the function to generate factors above. If a number has more than
    # one factor (excluding 1), it is not prime and thus will not be pushed to the true primes list.
    for elements in possible_prime_list:
        findfactors(elements)
        if len(factors_of_number) == 1:
            set_of_primes.append(elements)
        factors_of_number = []

    # KEY GENERATION
    # This loop runs for every single person on the 'people' list. It generates public and private key-value pairs for each contact.
    for each_person in range(len(people)):
        # The first 'large' prime is obtained from the previously created list.
        p = set_of_primes[random.randrange(0,len(set_of_primes))]
        # The second 'large' prime is similarly randomly obtained.
        q = set_of_primes[random.randrange(0,len(set_of_primes))]
        # The primes are multiplied to create the variable n. RSA is based on the principle that it is too difficult to determine
        # the individual primes that make up n if n is too large (hundreds of digits long, and not possible in this simulation).
        # This is known as the RSA or factoring problem, and to date, it has not been generally solved, unless a person should
        # have knowledge of hundred-digit primes which is a possibility unfeasible enough to warrant no consideration.
        n = int(p) * int(q)
        # The result of taking the totient function of the primes is also computed.
        tot_result = (p-1) * (q-1)

        # The following chunk of code is present to determine a coprime (preferably the first to maximize efficiency) to the totient
        # result by comparing the factors of j (the eventual coprime) to those of the variable tot_result.
        lower_limit = 2
        upper_limit = tot_result
        findfactors(upper_limit)
        upper_limit_factors = factors_of_number
        final_group = []
        for j in range(lower_limit, upper_limit+1):
            factors_of_number = []
            push = 0
            findfactors(j)
            j_factors = factors_of_number
            for j_elements in j_factors:
                for upper_limit_elements in upper_limit_factors:
                    if j_elements != upper_limit_elements:
                        push += 1
                    else:
                        push = 0
                        j += 1
            if push == len(j_factors) * len(upper_limit_factors):
                final_group.append(j_elements)
            else:
                push = 0
            if len(final_group) == len(j_factors) and upper_limit % j != 0:
                break

        # This block of code determines the smallest r and d such that one added to the totient result multiplied by r is divisible
        # by j. This eventually works to create the public and private key pairs.
        r = 1
        while float(tot_result*r+1) % float(j) != 0:
            r += 1
        d = int(float(tot_result*r+1)/float(j))

        # Here, the public key is created in a set containing the person's name and a tuple containing the previously determined j
        # and n.
        public_keys.append([people[people_index],(j,n)])

        # Similarly, the private key is also assembled although it will not be publicly displayed. The private key uses the tuple of
        # d and n.
        private_keys.append([people[people_index],(d,n)])

        # The public keys are publicly displayed so the user can see them, although the user will not actually need them to perform
        # a task. This actually simulates the user's computer or other appropriate device knowing the public key of the recipient
        # in order to successfully send an encrypted message.
        print public_keys[people_index][0],public_keys[people_index][1]

        # The function of the people index is to make the loop cycle through each person on the 'people' list. Without this line, the
        # keys of the first person on the list (in this case, Amy) would keep changing while Bob and Cathy were never assigned
        # keys.
        people_index += 1
        
    # USER INPUT, ENCRYPTION, AND DECRYPTION
    # Here, the user inputs the name of the person from the 'people' list that he/she would like to send an encrypted message to.
    receiver = raw_input("Receiver name: ")
    # The below is error handling. If the user inputs a name that is not on the list, integers, or even symbols, the program will
    # give him/her further chances to amend the choice.
    while receiver not in people:
        receiver = raw_input("Enter a name on the list. Try again: ")
    # As soon as the user inputs a name on the list, the program moves on from where it stalled in the while loop and continues in
    # the program.
    print "Your receiver is " + public_keys[people.index(receiver)][0] + "."
    # This is just a way for the user to visually see that his/her choice has been entered properly.
    print "The public entry is " + str(public_keys[people.index(receiver)]) + "."
    # This is the integer message that will ultimately be sent. The message cannot be in letter form as that is not handled by RSA.
    # However, letters and words can be sent through RSA using other ciphers or methods of converted letters to numbers. Generally,
    # as RSA is not meant to encrypt long strings of integers, it is used for simply sending the key to encrypted words while these
    # encrypted words can even be sent publicly, as without the key, the words cannot be decrypted.
    message = int(raw_input("Insert your message: "))
    # Below is the encrypted message. Based on the Euler-Fermat generalization, x will always be decrypted using the equation for the
    # decrypted message.
    x = pow(message,j) % n
    # This prints the encrypted message, and notifies the user that the message is being 'decrypted' on the 'other end' - which is
    # actually part of the same program.
    print "The encrypted message is " + str(x) + ".\nThe message has been sent.\nDecrypting..."
    # The modulo function simplifies the remainder until it is less than n. Unfortunately, if a user enters a message greater than n
    # - something that is not supposed to happen in RSA - the original message will not be equivalent to the decrypted message.
    # Hence, in order to prove that RSA still works regardless, n can be repeatedly added to return to the original message from a
    # possibly simplified one. This process is visible to the user after the line "Decrypting...."
    init_mult = 0
    # The decrypted message variable is initialized here.
    dec_message = 0
    while dec_message != message:
        dec_message = pow(x,d) % n + init_mult * n
        print dec_message
        init_mult += 1
    # This line prints the decrypted message to the user, so that it can be compared to the original one.
    print "The decrypted message is " + str(dec_message) + "."

    # RESTARTING THE PROGRAM
    # Here, the user is asked whether or not he/she would like to send another message, and is given the option to exit. If the user
    # inputs anything other than "No" (not case-sensitive), the program will continue.
    user_input = raw_input("Do you want to send another message? ")
    if user_input.lower() == "no":
        print "Exiting program..."
        status = False
