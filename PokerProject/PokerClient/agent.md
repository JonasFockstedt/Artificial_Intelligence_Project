# ♣♠♦♥ AI Poker Agent ♥♦♠♣

## Implemented Features

- Agent sorts its hand. Ascending rank order and in alphabetical suit order.
- Agent can determine which hand it has.
- Marks important cards when agent has pairs.
- Agent can determine if it is close to a straight (can only be determined by first or last card).
- Agent can determine if it is close to a flush (can only be determined by first or last card).
- Agent can see Ace as part of a low straight hand (A-2-3-4-5).
- If agent has "high cards" hand, it now sorts them in descending order in another list. This list can be used to determine how good "high cards" hand it has.

## Grading criteria

- Grade 3: A rational agent needs to be implemented.
- Grade 4: A reflex agent that takes the opponent's actions into account.
- Grade 5: An agent that can learn (e.g. with built-in machine learning algorithm) over time.

## TODO

- [ ] Rank hand.
  - [x] Determine the possible hands.
    - [x] High cards.
    - [x] One pair.
    - [x] Two pairs.
    - [x] Three of a kind.
    - [x] Straight.
    - [x] Flush.
    - [x] Full house.
    - [x] Four of a kind.
    - [x] Straight flush.
  - [ ] Rank strength of hand.
    - [ ] Give rank of the different type of hands.
    - [ ] Calculate strength of hand when agent has 'high cards'.
  - [ ] Rank potential strength.
    - [ ] Determine which goal hand is the closes.
- [ ] When to "check" during opening round (if first).
- [x] Handle cases when Aces are low (when part of a "A-2-3-4-5" straight or straight flush).
- [x] Mark important cards.
- [ ] Determine if close to flush

## IDEAS

### Hand

1. "Actual" ranking system. Used for determining the strength of current hand.
2. "Potential" ranking system. Used for determining how good the hand can become.

### Open Action

1. Depending of strength of hand.
2. _Check_ if low on chips (and first), to prevent unnecessary betting.

### Call / Raise Action

1. Based on number of chips left for the agent.
2. How close to a certain hand, i.e. if a possible good hand could be one round away, make sure to stay in the game.
3. Check current pot.

### Cards To Throw

1. Determine how close to a certain hand, called "goal" hand.
2. How far away the "goal" hand is (in number of rounds).
3. Have a way to mark a card as important (cards not to throw away). Could be in a separate list.

### Fold

1. If a certain percentage of chips has been bet during current round to a point that it is no longer sufficient.

### Check

1. When hand is mediocre.

# COMSOL

$c_r*sin(cosh((c_r-c_x)/c_r))$
$c_r$ = radie cirkel
$c_x$ = förflyttning i x-led
