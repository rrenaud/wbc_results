from collections import defaultdict

def GroupMatching(scores):
  last_ind = 0
  for ind, score in enumerate(scores):
    if score != scores[last_ind]:
      yield scores[last_ind:ind]
      last_ind = ind
  yield scores[last_ind:]

def RankifyGen(scores):
  cur_place = 1
  for group in GroupMatching(scores):
    excess_penalty = (len(group) - 1.0) / 2
    for score in group:
      yield cur_place + excess_penalty 
    cur_place += len(group)

def Rankify(scores):
  return list(RankifyGen(scores))

def AggregateOutcomes(outcomes):
  accum = defaultdict(int)
  for outcome in outcomes:
    accum[outcome] += 1
  ret = []
  for important_rank in [1, 1.5, 2, 2.5]:
    ret.append(accum[important_rank])
  return ret
    

def main():
  round_num = 1
  results_by_player = defaultdict(list)
  for line in open('results.txt'):
    if not line.strip():
        round_num += 1
        continue
    ranked_results = []
    player_entries = line.strip().split(',')
    for player_entry in player_entries:
      try:
        player, player_id, score = player_entry.split('-')
      except ValueError, e:
        print 'problem splitting', player_entry, 'at line', line
        return
      this_result = (-float(score), player, player_id)
      ranked_results.append(this_result)
    ranked_results.sort()
    parallel_ranks = Rankify(list(s[0] for s in ranked_results))

    for i in range(len(ranked_results)):
      _, player, player_id = ranked_results[i]
      results_by_player[(player, player_id)].append(parallel_ranks[i])

  aggregated_outcomes_with_player_and_id = [
    (player_with_id, AggregateOutcomes(result)) for player_with_id, result in
     results_by_player.iteritems()]
  aggregated_outcomes_with_player_and_id.sort(key=lambda g: g[1], reverse=True)

  print 'rank\tname\t\t\tid\tfirsts\tseconds'
  for rank, ((player, player_id), outcomes) in enumerate(
      aggregated_outcomes_with_player_and_id):
    assert outcomes[1] == 0 and outcomes[3] == 0, '%s %s %s' % (player, player_id, str(outcomes))
    print str(rank + 1).ljust(8), player.ljust(24), str(player_id).ljust(7), \
      str(outcomes[0]).ljust(8), str(outcomes[2]).ljust(8)


if __name__ == '__main__':
  main()

