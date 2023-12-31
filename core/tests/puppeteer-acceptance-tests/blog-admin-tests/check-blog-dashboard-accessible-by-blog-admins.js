// Copyright 2023 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Accpetance Test for a Super Admin assign Blog Admin role.
 */

const userFactory = require(
  '../puppeteer-testing-utilities/user-factory.js');

let checkBlogDashboardAccessibleByBlogAdmins = async function() {
  const guestUser = await userFactory.createNewGuestUser(
    'guestUser', 'guest_user@example.com');
  const blogAdmin = await userFactory.createNewBlogAdmin('blogAdm');

  /** The blog-dashboard is not accessible to any guest user
   *  as the user does not have the blog admin role. */
  await guestUser.expectBlogDashboardAccessToBeUnauthorized();

  await blogAdmin.expectBlogDashboardAccessToBeAuthorized();

  await userFactory.closeAllBrowsers();
};

checkBlogDashboardAccessibleByBlogAdmins();
