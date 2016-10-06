In order to test the functionality for the following problems, run the given command in command line:

2B: Standard Spellcheck: This will take an inputted file, and output the corrected version in corrected.txt

python spellcheck.py <ToBeSpellCheckedFileName> 3esl.txt
	ex. python spellcheck.py text.txt 3esl.txt

2C: Measure Error: This will take an inputted file that contains several lines of pairs of words.  The first word in the pair is the typo, the second word in the pair is the correct version of the word.  This command will correct each of the typo words, and then compare it to the correct version in order to measure error.

python spellcheck.py <ToBeSpellCheckedFileName> 3esl.txt 1
	ex. python spellcheck.py wikipediatypo.txt 3esl.txt 14A: Qwerty Measure Error: This will take an inputted file that contains several lines of pairs of words.  The first word in the pair is the typo, the second word in the pair is the correct version of the word.  This command will correct each of the typo words, and then compare it to the correct version in order to measure error. In this algorithm it will use the qwerty version of the methods to assess substitution cost.

python spellcheck.py <ToBeSpellCheckedFileName> 3esl.txt 2
	ex. python spellcheck.py wikipediatypo.txt 3esl.txt 2

3C: First Experiment: This will take a sample set of size 35, and test 64 combinations in order to determine the best parameter.

python spellcheck.py wikipediatypo.txt 3esl.txt 3

4B: Second Experiment: This will take a sample set of size 35, and test 16 combinations in order to determine the best parameter. This experiment utilizes the qwerty distance method.

python spellcheck.py wikipediatypo.txt 3esl.txt 3
