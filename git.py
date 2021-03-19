import datetime
import re
import ujson

from pydriller.metrics.process.change_set import ChangeSet
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from pydriller.metrics.process.contributors_count import ContributorsCount
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.hunks_count import HunksCount
from pydriller.metrics.process.lines_count import LinesCount


class GitProcessor:
    def __init__(self, url):
        self.url = url
        if re.match(r'^http(s)?://(www\.)?github.com/.+/.+', url):
            # Github repo
            # rm = RepositoryMining(url)
            print(f'Inspecting: {url}')
            # for commit in rm.traverse_commits():
            #     print("| {} | {} | {} | {} |".format(
            #         commit.msg,
            #         commit.dmm_unit_size,
            #         commit.dmm_unit_complexity,
            #         commit.dmm_unit_interfacing
            #     ))
        elif re.match(r'^http(s)?://(www\.)?github.com/.+', url):
            # Github org
            raise NotImplementedError
        elif url.startswith('https://gitlab.com/'):
            raise NotImplementedError
        elif re.match(r'^http(s)?://gitlab\..*/.*', url):
            raise NotImplementedError
        elif url.startswith('https://bitbucket.org/'):
            raise NotImplementedError
        elif url.startswith('https://etherscan.io/address/'):
            raise NotImplementedError
        elif url.startswith('https://etherscan.io/token/'):
            raise NotImplementedError
        elif url.startswith('https://bscscan.com/address/'):
            raise NotImplementedError
        else:
            raise Exception(f'Repository not supported: {url}')

    def fetch_metrics(self):
        change_set = ChangeSet(self.url, since=datetime.datetime.fromtimestamp(0), to=datetime.datetime.now())
        code_churn = CodeChurn(self.url, since=datetime.datetime.fromtimestamp(0), to=datetime.datetime.now())
        commits_count = CommitsCount(self.url, since=datetime.datetime.fromtimestamp(0), to=datetime.datetime.now())
        contributors_count = ContributorsCount(self.url, since=datetime.datetime.fromtimestamp(0),
                                               to=datetime.datetime.now())
        contributors_experience = ContributorsExperience(self.url, since=datetime.datetime.fromtimestamp(0),
                                                         to=datetime.datetime.now())
        hunks_count = HunksCount(self.url, since=datetime.datetime.fromtimestamp(0), to=datetime.datetime.now())
        line_count = LinesCount(self.url, since=datetime.datetime.fromtimestamp(0), to=datetime.datetime.now())
        return {
            'changeSet': change_set,
            'codeChurn': code_churn,
            'commitsCount': commits_count,
            'contributorsCount': contributors_count,
            'contributorsExperience': contributors_experience,
            'hunksCount': hunks_count,
            'lineCount': line_count,
        }


if __name__ == '__main__':
    with open("coins-full.json", "r") as coins_full_file:
        all_items = ujson.load(coins_full_file)
        print(f'Processing all {len(all_items)} items')
        for item in all_items:
            for source in item['urls']['source_code']:
                try:
                    processor = GitProcessor(source)
                    print(processor.fetch_metrics())
                except Exception as e:
                    print(f'Could not process item: {item["symbol"]}: {e}')
