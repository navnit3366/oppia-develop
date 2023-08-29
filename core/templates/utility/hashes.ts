// Copyright 2022 The Oppia Authors. All Rights Reserved.
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
 * @fileoverview File that exports that hashes that are generated by our build
 * process.
 */


// Relative path used as an work around to get the angular compiler and webpack
// build to not complain.
// Webpack absolute import is just "hashes.json".
// AoT version is "assets/hashes.json".
// TODO(#16309): Fix relative imports.
import resourceHashes from '../../../assets/hashes.json';

export default {
  _hashes: resourceHashes as Record<string, string>,
  get hashes(): Record<string, string> {
    return resourceHashes as Record<string, string>;
  }
};
