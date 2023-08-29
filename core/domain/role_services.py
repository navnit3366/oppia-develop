# coding: utf-8
#
# Copyright 2017 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module contains the structure of roles and actions,
actions permitted to the roles and the functions needed to access roles
and actions.
"""

from __future__ import annotations

import copy
import math
import random
import time

from core import feconf
from core.platform import models

from typing import Dict, List, Optional

MYPY = False
if MYPY: # pragma: no cover
    from mypy_imports import audit_models

(audit_models,) = models.Registry.import_models([models.Names.AUDIT])

# Actions that can be performed in the system.
ACTION_ACCEPT_ANY_SUGGESTION = 'ACCEPT_ANY_SUGGESTION'
ACTION_ACCESS_CREATOR_DASHBOARD = 'ACCESS_CREATOR_DASHBOARD'
ACTION_ACCESS_LEARNER_DASHBOARD = 'ACCESS_LEARNER_DASHBOARD'
ACTION_ACCESS_MODERATOR_PAGE = 'ACCESS_MODERATOR_PAGE'
ACTION_ACCESS_RELEASE_COORDINATOR_PAGE = 'ACCESS_RELEASE_COORDINATOR_PAGE'
ACTION_ACCESS_BLOG_DASHBOARD = 'ACCESS_BLOG_DASHBOARD'
ACTION_ACCESS_BLOG_ADMIN_PAGE = 'ACCESS_BLOG_ADMIN_PAGE'
ACTION_ACCESS_TOPICS_AND_SKILLS_DASHBOARD = 'ACCESS_TOPICS_AND_SKILLS_DASHBOARD'
ACTION_ACCESS_CONTRIBUTOR_DASHBOARD_ADMIN_PAGE = (
    'ACCESS_CONTRIBUTOR_DASHBOARD_ADMIN_PAGE')
ACTION_CHANGE_TOPIC_STATUS = 'CHANGE_TOPIC_STATUS'
ACTION_CHANGE_STORY_STATUS = 'CHANGE_STORY_STATUS'
ACTION_CREATE_COLLECTION = 'CREATE_COLLECTION'
ACTION_CREATE_EXPLORATION = 'CREATE_EXPLORATION'
ACTION_CREATE_NEW_SKILL = 'CREATE_NEW_SKILL'
ACTION_CREATE_NEW_TOPIC = 'CREATE_NEW_TOPIC'
ACTION_MANAGE_QUESTION_SKILL_STATUS = 'MANAGE_QUESTION_SKILL_STATUS'
ACTION_DELETE_ANY_ACTIVITY = 'DELETE_ANY_ACTIVITY'
ACTION_DELETE_ANY_BLOG_POST = 'DELETE_ANY_BLOG_POST'
ACTION_DELETE_ANY_PUBLIC_ACTIVITY = 'DELETE_ANY_PUBLIC_ACTIVITY'
ACTION_DELETE_ANY_QUESTION = 'DELETE_ANY_QUESTION'
ACTION_DELETE_ANY_SKILL = 'DELETE_ANY_SKILL'
ACTION_DELETE_OWNED_PRIVATE_ACTIVITY = 'DELETE_OWNED_PRIVATE_ACTIVITY'
ACTION_DELETE_TOPIC = 'DELETE_TOPIC'
ACTION_EDIT_ANY_ACTIVITY = 'EDIT_ANY_ACTIVITY'
ACTION_EDIT_ANY_BLOG_POST = 'EDIT_ANY_BLOG_POST'
ACTION_EDIT_ANY_PUBLIC_ACTIVITY = 'EDIT_ANY_PUBLIC_ACTIVITY'
ACTION_EDIT_ANY_QUESTION = 'EDIT_ANY_QUESTION'
ACTION_EDIT_ANY_SKILL = 'EDIT_ANY_SKILL'
ACTION_EDIT_ANY_SUBTOPIC_PAGE = 'EDIT_ANY_SUBTOPIC_PAGE'
ACTION_EDIT_ANY_TOPIC = 'EDIT_ANY_TOPIC'
ACTION_RUN_ANY_JOB = 'RUN_ANY_JOB'
ACTION_EDIT_ANY_STORY = 'EDIT_ANY_STORY'
ACTION_EDIT_OWNED_ACTIVITY = 'EDIT_OWNED_ACTIVITY'
ACTION_EDIT_OWNED_TOPIC = 'EDIT_OWNED_TOPIC'
ACTION_EDIT_OWNED_STORY = 'EDIT_OWNED_STORY'
ACTION_EDIT_SKILL_DESCRIPTION = 'EDIT_SKILL_DESCRIPTION'
ACTION_EDIT_SKILL = 'EDIT_SKILL'
ACTION_FLAG_EXPLORATION = 'FLAG_EXPLORATION'
ACTION_MANAGE_ACCOUNT = 'MANAGE_ACCOUNT'
ACTION_MANAGE_TRANSLATION_CONTRIBUTOR_ROLES = 'MANAGE_TRANSLATION_ROLES'
ACTION_MANAGE_QUESTION_CONTRIBUTOR_ROLES = 'MANAGE_QUESTION_ROLES'
ACTION_MANAGE_MEMCACHE = 'MANAGE_MEMCACHE'
ACTION_MANAGE_QUESTION_RIGHTS = 'MANAGE_QUESTION_RIGHTS'
ACTION_MANAGE_TOPIC_RIGHTS = 'MANAGE_TOPIC_RIGHTS'
ACTION_MANAGE_BLOG_POST_EDITORS = 'MANAGE_BLOG_POST_EDITORS'
ACTION_MODIFY_CORE_ROLES_FOR_ANY_ACTIVITY = 'MODIFY_CORE_ROLES_FOR_ANY_ACTIVITY'
ACTION_MODIFY_CORE_ROLES_FOR_OWNED_ACTIVITY = (
    'MODIFY_CORE_ROLES_FOR_OWNED_ACTIVITY')
ACTION_PLAY_ANY_PRIVATE_ACTIVITY = 'PLAY_ANY_PRIVATE_ACTIVITY'
ACTION_PLAY_ANY_PUBLIC_ACTIVITY = 'PLAY_ANY_PUBLIC_ACTIVITY'
ACTION_PUBLISH_ANY_ACTIVITY = 'PUBLISH_ANY_ACTIVITY'
ACTION_PUBLISH_OWNED_ACTIVITY = 'PUBLISH_OWNED_ACTIVITY'
ACTION_PUBLISH_OWNED_SKILL = 'PUBLISH_OWNED_SKILL'
ACTION_RATE_ANY_PUBLIC_EXPLORATION = 'RATE_ANY_PUBLIC_EXPLORATION'
ACTION_SEND_MODERATOR_EMAILS = 'SEND_MODERATOR_EMAILS'
ACTION_SUBSCRIBE_TO_USERS = 'SUBSCRIBE_TO_USERS'
ACTION_SUGGEST_CHANGES = 'SUGGEST_CHANGES'
ACTION_UNPUBLISH_ANY_PUBLIC_ACTIVITY = 'UNPUBLISH_ANY_PUBLIC_ACTIVITY'
ACTION_VISIT_ANY_QUESTION_EDITOR_PAGE = 'VISIT_ANY_QUESTION_EDITOR_PAGE'
ACTION_VISIT_ANY_TOPIC_EDITOR_PAGE = 'VISIT_ANY_TOPIC_EDITOR_PAGE'
ACTION_CAN_MANAGE_VOICE_ARTIST = 'CAN_MANAGE_VOICE_ARTIST'
ACTION_ACCESS_LEARNER_GROUPS = 'ACCESS_LEARNER_GROUPS'

# Users can be updated to the following list of role IDs via admin interface.
#
# NOTE: LEARNER role should not be updated to any other role, hence do not
#   add it to the following list.
UPDATABLE_ROLES = [
    feconf.ROLE_ID_BLOG_ADMIN,
    feconf.ROLE_ID_CURRICULUM_ADMIN,
    feconf.ROLE_ID_COLLECTION_EDITOR,
    feconf.ROLE_ID_FULL_USER,
    feconf.ROLE_ID_VOICEOVER_ADMIN,
    feconf.ROLE_ID_MODERATOR,
    feconf.ROLE_ID_QUESTION_ADMIN,
    feconf.ROLE_ID_RELEASE_COORDINATOR,
    feconf.ROLE_ID_TOPIC_MANAGER,
    feconf.ROLE_ID_TRANSLATION_ADMIN,
]

# Users can be viewed by following list of role IDs via admin interface.
#
# NOTE: Do not include MOBILE_LEARNER role in this list as it does not represent
#   role for a separate user account, but rather a profile within the account.
VIEWABLE_ROLES = [
    feconf.ROLE_ID_BLOG_ADMIN,
    feconf.ROLE_ID_BLOG_POST_EDITOR,
    feconf.ROLE_ID_COLLECTION_EDITOR,
    feconf.ROLE_ID_CURRICULUM_ADMIN,
    feconf.ROLE_ID_MODERATOR,
    feconf.ROLE_ID_QUESTION_ADMIN,
    feconf.ROLE_ID_RELEASE_COORDINATOR,
    feconf.ROLE_ID_TOPIC_MANAGER,
    feconf.ROLE_ID_TRANSLATION_ADMIN,
    feconf.ROLE_ID_VOICEOVER_ADMIN,
]

# The string corresponding to role IDs that should be visible to admin.
HUMAN_READABLE_ROLES = {
    feconf.ROLE_ID_BLOG_ADMIN: 'blog admin',
    feconf.ROLE_ID_BLOG_POST_EDITOR: 'blog post editor',
    feconf.ROLE_ID_COLLECTION_EDITOR: 'collection editor',
    feconf.ROLE_ID_CURRICULUM_ADMIN: 'curriculum admin',
    feconf.ROLE_ID_FULL_USER: 'full user',
    feconf.ROLE_ID_GUEST: 'guest',
    feconf.ROLE_ID_MOBILE_LEARNER: 'mobile learner',
    feconf.ROLE_ID_MODERATOR: 'moderator',
    feconf.ROLE_ID_QUESTION_ADMIN: 'question admin',
    feconf.ROLE_ID_RELEASE_COORDINATOR: 'release coordinator',
    feconf.ROLE_ID_TOPIC_MANAGER: 'topic manager',
    feconf.ROLE_ID_TRANSLATION_ADMIN: 'translation admin',
    feconf.ROLE_ID_VOICEOVER_ADMIN: 'voiceover admin',
}


# This dict represents all the actions that belong to a particular role.
_ROLE_ACTIONS = {
    feconf.ROLE_ID_CURRICULUM_ADMIN: [
        ACTION_ACCEPT_ANY_SUGGESTION,
        ACTION_ACCESS_TOPICS_AND_SKILLS_DASHBOARD,
        ACTION_CHANGE_STORY_STATUS,
        ACTION_CHANGE_TOPIC_STATUS,
        ACTION_CREATE_NEW_SKILL,
        ACTION_CREATE_NEW_TOPIC,
        ACTION_DELETE_ANY_ACTIVITY,
        ACTION_DELETE_ANY_QUESTION,
        ACTION_DELETE_ANY_SKILL,
        ACTION_DELETE_TOPIC,
        ACTION_EDIT_ANY_ACTIVITY,
        ACTION_EDIT_ANY_QUESTION,
        ACTION_EDIT_ANY_STORY,
        ACTION_EDIT_ANY_SUBTOPIC_PAGE,
        ACTION_EDIT_ANY_TOPIC,
        ACTION_EDIT_SKILL,
        ACTION_EDIT_SKILL_DESCRIPTION,
        ACTION_EDIT_OWNED_TOPIC,
        ACTION_MANAGE_QUESTION_SKILL_STATUS,
        ACTION_MANAGE_TOPIC_RIGHTS,
        ACTION_MODIFY_CORE_ROLES_FOR_ANY_ACTIVITY,
        ACTION_PUBLISH_ANY_ACTIVITY,
        ACTION_PUBLISH_OWNED_SKILL,
        ACTION_VISIT_ANY_QUESTION_EDITOR_PAGE,
        ACTION_VISIT_ANY_TOPIC_EDITOR_PAGE
    ],
    feconf.ROLE_ID_COLLECTION_EDITOR: [
        ACTION_CREATE_COLLECTION
    ],
    feconf.ROLE_ID_FULL_USER: [
        ACTION_ACCESS_CREATOR_DASHBOARD,
        ACTION_ACCESS_LEARNER_DASHBOARD,
        ACTION_ACCESS_LEARNER_GROUPS,
        ACTION_CREATE_EXPLORATION,
        ACTION_DELETE_OWNED_PRIVATE_ACTIVITY,
        ACTION_EDIT_OWNED_ACTIVITY,
        ACTION_FLAG_EXPLORATION,
        ACTION_MANAGE_ACCOUNT,
        ACTION_MODIFY_CORE_ROLES_FOR_OWNED_ACTIVITY,
        ACTION_PLAY_ANY_PUBLIC_ACTIVITY,
        ACTION_PUBLISH_OWNED_ACTIVITY,
        ACTION_RATE_ANY_PUBLIC_EXPLORATION,
        ACTION_SUBSCRIBE_TO_USERS,
        ACTION_SUGGEST_CHANGES
    ],
    feconf.ROLE_ID_GUEST: [
        ACTION_PLAY_ANY_PUBLIC_ACTIVITY
    ],
    feconf.ROLE_ID_MOBILE_LEARNER: [
        ACTION_PLAY_ANY_PUBLIC_ACTIVITY
    ],
    feconf.ROLE_ID_MODERATOR: [
        ACTION_ACCESS_MODERATOR_PAGE,
        ACTION_DELETE_ANY_ACTIVITY,
        ACTION_DELETE_ANY_PUBLIC_ACTIVITY,
        ACTION_EDIT_ANY_ACTIVITY,
        ACTION_EDIT_ANY_PUBLIC_ACTIVITY,
        ACTION_PLAY_ANY_PRIVATE_ACTIVITY,
        ACTION_SEND_MODERATOR_EMAILS,
        ACTION_UNPUBLISH_ANY_PUBLIC_ACTIVITY,
        ACTION_MODIFY_CORE_ROLES_FOR_ANY_ACTIVITY
    ],
    feconf.ROLE_ID_RELEASE_COORDINATOR: [
        ACTION_ACCESS_RELEASE_COORDINATOR_PAGE,
        ACTION_MANAGE_MEMCACHE,
        ACTION_RUN_ANY_JOB,
    ],
    feconf.ROLE_ID_TOPIC_MANAGER: [
        ACTION_ACCESS_TOPICS_AND_SKILLS_DASHBOARD,
        ACTION_DELETE_ANY_QUESTION,
        ACTION_EDIT_ANY_QUESTION,
        ACTION_EDIT_OWNED_STORY,
        ACTION_EDIT_OWNED_TOPIC,
        ACTION_EDIT_SKILL,
        ACTION_EDIT_ANY_SUBTOPIC_PAGE,
        ACTION_MANAGE_QUESTION_SKILL_STATUS,
        ACTION_VISIT_ANY_QUESTION_EDITOR_PAGE,
        ACTION_VISIT_ANY_TOPIC_EDITOR_PAGE
    ],
    feconf.ROLE_ID_VOICEOVER_ADMIN: [ACTION_CAN_MANAGE_VOICE_ARTIST],
    feconf.ROLE_ID_QUESTION_ADMIN: [
        ACTION_ACCESS_CONTRIBUTOR_DASHBOARD_ADMIN_PAGE,
        ACTION_MANAGE_QUESTION_CONTRIBUTOR_ROLES
    ],
    feconf.ROLE_ID_TRANSLATION_ADMIN: [
        ACTION_ACCESS_CONTRIBUTOR_DASHBOARD_ADMIN_PAGE,
        ACTION_MANAGE_TRANSLATION_CONTRIBUTOR_ROLES
    ],
    feconf.ROLE_ID_BLOG_ADMIN: [
        ACTION_ACCESS_BLOG_ADMIN_PAGE,
        ACTION_ACCESS_BLOG_DASHBOARD,
        ACTION_DELETE_ANY_BLOG_POST,
        ACTION_EDIT_ANY_BLOG_POST,
        ACTION_MANAGE_BLOG_POST_EDITORS
    ],
    feconf.ROLE_ID_BLOG_POST_EDITOR: [
        ACTION_ACCESS_BLOG_DASHBOARD
    ]
}


def get_all_actions(roles: List[str]) -> List[str]:
    """Returns a list of all actions that can be performed by the given role.

    Args:
        roles: list(str). A list of strings defining the user roles.

    Returns:
        list(str). A list of actions accessible to the role.

    Raises:
        Exception. The given role does not exist.
    """
    role_actions = set()
    for role in roles:
        if role not in _ROLE_ACTIONS:
            raise Exception('Role %s does not exist.' % role)

        role_actions |= set(_ROLE_ACTIONS[role])

    return list(role_actions)


def get_role_actions() -> Dict[str, List[str]]:
    """Returns the possible role to actions items in the application.

    Returns:
        dict(str, list(str)). A dict presenting key as role and values as list
        of actions corresponding to the given role.
    """
    return copy.deepcopy(_ROLE_ACTIONS)


def log_role_query(
    user_id: str,
    intent: str,
    role: Optional[str] = None,
    username: Optional[str] = None
) -> None:
    """Stores the query to role structure in RoleQueryAuditModel."""
    model_id = '%s.%s.%s.%s' % (
        user_id, int(math.floor(time.time())), intent, random.randint(0, 1000)
    )

    model = audit_models.RoleQueryAuditModel(
        id=model_id, user_id=user_id, intent=intent,
        role=role, username=username)
    model.update_timestamps()
    model.put()
