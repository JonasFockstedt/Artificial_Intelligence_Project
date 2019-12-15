# IDEAS

## TODO
- [ ] Rank hand.
    - [ ] Determine the possible hands.
        - [ ] High cards.
        - [x] One pair.
        - [x] Two pairs.
        - [x] Three of a kind.
        - [x] Straight.
        - [x] Flush.
        - [x] Full house.
        - [x] Four of a kind.
        - [x] Straight flush.
    - [x] Rank actual strength. Adding value of ranks.
    - [ ] Rank potential strength.
- [ ] When to "check" during opening round (if first).
- [x] Determine if hand consists of two pairs.

### Hand
1. "Actual" ranking system. Used for determining the strength of current hand.
2. "Potential" ranking system. Used for determining how good the hand can become.

### Open Action
1. Depending of strength of hand.
2. *Check* if low on chips (and first), to prevent unnecessary betting.

### Call / Raise Action
1. Based on number of chips left for the agent.
2. How close to a certain hand, i.e. if a possible good hand could be one round away, make sure to stay in the game.
3. Check current pot.

### Cards To Throw
1. Determine how close to a certain hand. 
2. How far away the "goal" hand is (in number of rounds).
3. Have a way to mark a card as important (cards not to throw away). Could be in a separate list.

### Fold
1. If a certain percentage of chips has been bet during current round to a point that it is no longer sufficient.

