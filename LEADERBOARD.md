# New Restaurant Voting Leaderboard Feature

A cool new leaderboard API has been added to provide real-time insights into the restaurant voting competition!

## API Endpoint

```
GET /api/leaderboard
```

Returns a JSON response containing:
- Current rankings of all restaurants with vote counts
- Total votes across all restaurants
- Current leader and their vote count
- Closest race between restaurants (smallest vote gap)
- Timestamp of the response

Example response:
```json
{
    "rankings": [
        {
            "name": "outback",
            "votes": 42,
            "rank": 1
        },
        ...
    ],
    "stats": {
        "total_votes": 156,
        "leader": "outback",
        "leader_votes": 42,
        "closest_race": "outback vs chipotle",
        "vote_gap": 3
    },
    "timestamp": "2023-07-20T15:30:00"
}
```

## Features
- Real-time vote tracking
- Restaurant rankings
- Vote gap analysis showing closest competitions
- Total vote statistics
- ISO 8601 timestamp for tracking updates

The leaderboard brings an exciting competitive element to the voting app by showing:
- Which restaurant is winning
- How close the races are
- Total community engagement through vote counts