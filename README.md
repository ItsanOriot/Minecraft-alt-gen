# Minecraft-alt-gen

Discord bot which generates accounts from a txt file. Has a fully working key system which tracks sub dates so you can integrate into a shoppy/autobuy service. There are multiple tiers of keys, each one has a different daily limit of how many accounts they can generate every 24h.

This was initially sold to a friend, but he scammed someone and then dropped off the face of the earth so Ill just put this up lol.
Also has some random stuff I added cuz I was bored.

ok so dont fuck with the files cuz the thingy relies on them having the right name
you can refill keys by opening the key file and just pasting in more keys, just make sure the keys dont have ' " [ ] { } ( or ) in them
it should be able to handle as many keys as u want, but putting in too many keys at 1 time will slow it down, so stick to max like ~50-75 keys in stock at a time
you can delete any keys from the list (dont reccomend it cuz ull scam someone by stealing their key) but make sure you dont delete the last line (that fillerchungus line) cuz that line wont work



wait until console print "initiated" before running any commands

daily generations reset at midnight every night in your timezone

u need to name the roles for each plan "basic", "vip", "premium", and "royalty"
I can change the names if u ask, but make sure the role names are that

ur pc needs python 3.9.2 or higher
you need to install every library on requirements.txt by going to command prompt and typing: pip install <requirement>


change the token in "client.run" at the end of the file to the token of your bot
make sure your bot has admin
