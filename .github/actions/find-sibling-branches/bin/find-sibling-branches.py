#!/usr/bin/env python
import urllib.request
import json
import os

import yaml
from ghapi.all import GhApi, paged

from alp.common import ActionAdapter


def is_branch_in_pager(pager, branch):
    for page in pager:
        for page_branch in page:
            if branch == page_branch['name']:
                return True
    return False


def find_packages_to_build(api, repos, branch):
    to_build = {}
    for name, repo in repos.items():
        pager = paged(api.repos.list_branches, *repo.split('/'))
        if is_branch_in_pager(pager, branch):
            to_build[name] = repo
    return to_build


def main(repos, is_rebuild, sibling_ref):
    if is_rebuild != 'true':
        api = GhApi()
        repos = find_packages_to_build(api, repos, sibling_ref)

    return dict(repos=repos)


if __name__ == '__main__':
    ActionAdapter(main)
