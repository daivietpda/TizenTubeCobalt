# Copyright 2017 The Cobalt Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Base cobalt configuration for GYP."""

from starboard.build import application_configuration
from starboard.tools.testing import test_filter

# The canonical Cobalt application name.
APPLICATION_NAME = 'cobalt'

# A map of failing or crashing tests per target
# pylint: disable=line-too-long
_FILTERED_TESTS = {
    'base_unittests': [
        # TODO: b/329269559 These have flaky ASAN heap-use-after-free
        # during metrics collection.
        'All/SequenceManagerTest.DelayedTasksDontBadlyStarveNonDelayedWork_DifferentQueue/WithMessagePump',
        'All/SequenceManagerTest.DelayedTasksDontBadlyStarveNonDelayedWork_DifferentQueue/WithMessagePumpAlignedWakeUps',
        'All/SequenceManagerTest.DelayedTasksDontBadlyStarveNonDelayedWork_DifferentQueue/WithMockTaskRunner',
        'All/SequenceManagerTest.DelayedTasksDontBadlyStarveNonDelayedWork_SameQueue/WithMessagePump',
        'All/SequenceManagerTest.DelayedTasksDontBadlyStarveNonDelayedWork_SameQueue/WithMessagePumpAlignedWakeUps',
        'All/SequenceManagerTest.DelayedTasksDontBadlyStarveNonDelayedWork_SameQueue/WithMockTaskRunner',
        'All/SequenceManagerTest.SweepCanceledDelayedTasks_ManyTasks/WithMessagePump',
        'All/SequenceManagerTest.SweepCanceledDelayedTasks_ManyTasks/WithMessagePumpAlignedWakeUps',
        'All/SequenceManagerTest.SweepCanceledDelayedTasks_ManyTasks/WithMockTaskRunner',
        # TODO: b/329507754 - Flaky after recent rebase.
        'ScopedBlockingCallIOJankMonitoringTest.MultiThreadedOverlappedWindows',
        'TaskEnvironmentTest.MultiThreadedMockTimeAndThreadPoolQueuedMode'
    ],
    'net_unittests': [
        # TODO: b/329507754 - Flaky after recent rebase.
        'CookieMonsterTest.DeleteExpiredPartitionedCookiesAfterTimeElapsed',

        # TODO: b/331469815 - Hangs in GitHub actions.
        'TCPClientSocketTest.*',

        # TODO: b/327008491 - Unused functionality but should be enabled.
        'DiskCacheTest.*',
        'DiskCacheBackendTest.*',
        'DiskCacheEntryTest.*',
        'CacheUtilTest.*',
        'SimpleFileTrackerTest.*',
        'SimpleIndexFileTest.*',
        'SimpleVersionUpgradeTest.*',
        '*FileNetLogObserver*',
    ]
}


class CobaltConfiguration(application_configuration.ApplicationConfiguration):
  """Base Cobalt configuration class.

  Cobalt per-platform configurations, if defined, must subclass from this class.
  """

  def GetTestFilters(self):
    filters = super().GetTestFilters()
    for target, tests in _FILTERED_TESTS.items():
      filters.extend(test_filter.TestFilter(target, test) for test in tests)
    return filters

  def GetWebPlatformTestFilters(self):
    """Gets all tests to be excluded from a black box test run."""

    # Skipped tests on all platforms due to HTTP proxy bugs.
    # Tests pass with a direct SSH tunnel.
    # Proxy sends out response lines as soon as it gets it without waiting
    # for the entire response. It is possible that this causes issues or that
    # the proxy has problems sending and terminating a single complete
    # response. It may end up sending multiple empty responses.
    filters = [
        # CORS - 304 checks
        # Disabled because of: Flaky on buildbot, proxy unreliability
        'cors/WebPlatformTest.Run/cors_304_htm',

        # Late listeners: Preflight.
        # Disabled because of: Flaky. Buildbot only failure.
        'cors/WebPlatformTest.Run/cors_late_upload_events_htm',

        # getResponseHeader: Combined testing of cors response headers.
        # Disabled because of: Timeout.
        'cors/WebPlatformTest.Run/cors_response_headers_htm',

        # Status on GET 400, HEAD 401, POST 404, PUT 200.
        # Disabled because of: Response status returning 0.
        'cors/WebPlatformTest.Run/cors_status_async_htm',

        # CORS - status after preflight on POST 401, POST 404, PUT 699.
        # Disabled because of: Response status returning 0 or timeout.
        'cors/WebPlatformTest.Run/cors_status_preflight_htm',

        # Response reader closed promise should reject after a network error
        # happening after resolving fetch promise.
        # Disabled because of: Timeout.
        'fetch/WebPlatformTest.Run/fetch_api_basic_error_after_response_html',

        # RequestCache "no-store" mode does not store the response in the
        # cache with Last-Modified and fresh response.
        # Disabled because of: Timeout. Buildbot only failure.
        ('fetch/WebPlatformTest.Run/'
         'fetch_api_request_request_cache_no_store_html'),

        # RequestCache "no-cache" mode revalidates fresh responses found in
        # the cache.
        # Disabled because of: Caching bug.
        ('fetch/WebPlatformTest.Run/'
         'fetch_api_request_request_cache_no_cache_html'),

        # Check response clone use structureClone for teed ReadableStreams
        # (DataViewchunk).
        # Disabled because of: Timeout.
        'fetch/WebPlatformTest.Run/fetch_api_response_response_clone_html',

        # XMLHttpRequest: send() - Basic authenticated CORS request using
        # setRequestHeader().
        # Disabled because of: Timeout. Buildbot only failure.
        ('xhr/WebPlatformTest.Run/'
         'XMLHttpRequest_cobalt_trunk_send_authentication_cors_basic_'
         'setrequestheader_htm'),

        # XMLHttpRequest: send() - CORS request with setRequestHeader auth to
        # URL accepting Authorization header.
        # Disabled because of: False user and password. Buildbot only failure.
        ('xhr/WebPlatformTest.Run/'
         'XMLHttpRequest_cobalt_trunk_send_authentication_cors_'
         'setrequestheader_no_cred_htm'),

        # XMLHttpRequest: send() - Redirects (basics) (307).
        # Disabled because of: Flaky.
        'xhr/WebPlatformTest.Run/XMLHttpRequest_send_redirect_htm',

        # Disabled because of: Flaky on buildbot across multiple buildconfigs.
        # Non-reproducible with local runs.
        ('xhr/WebPlatformTest.Run/'
         'XMLHttpRequest_send_entity_body_get_head_async_htm'),
        'xhr/WebPlatformTest.Run/XMLHttpRequest_status_error_htm',
        'xhr/WebPlatformTest.Run/XMLHttpRequest_response_json_htm',
        'xhr/WebPlatformTest.Run/XMLHttpRequest_send_redirect_to_non_cors_htm',

        # pylint: disable=line-too-long
        # b/332367155
        'websockets/WebPlatformTest.Run/websockets_closing_handshake_002_html',
        'websockets/WebPlatformTest.Run/websockets_closing_handshake_004_html',
        'websockets/WebPlatformTest.Run/websockets_binary_001_html',
        'websockets/WebPlatformTest.Run/websockets_binary_002_html',
        'websockets/WebPlatformTest.Run/websockets_binary_004_html',
        'websockets/WebPlatformTest.Run/websockets_binary_005_html',
        'websockets/WebPlatformTest.Run/websockets_constructor_006_html',
        'websockets/WebPlatformTest.Run/websockets_constructor_009_html',
        'websockets/WebPlatformTest.Run/websockets_constructor_013_html',
        'websockets/WebPlatformTest.Run/websockets_constructor_022_html',
        'websockets/WebPlatformTest.Run/websockets_cookies_001_html',
        'websockets/WebPlatformTest.Run/websockets_cookies_006_html',
        'websockets/WebPlatformTest.Run/websockets_extended_payload_length_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_bufferedAmount_bufferedAmount_arraybuffer_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_bufferedAmount_bufferedAmount_blob_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_bufferedAmount_bufferedAmount_getting_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_bufferedAmount_bufferedAmount_large_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_bufferedAmount_bufferedAmount_unicode_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_events_015_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_events_016_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_events_017_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_readyState_008_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_send_007_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_send_008_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_send_009_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_send_010_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_send_011_html',
        'websockets/WebPlatformTest.Run/websockets_interfaces_WebSocket_send_012_html',
        'websockets/WebPlatformTest.Run/websockets_keeping_connection_open_001_html',
        'websockets/WebPlatformTest.Run/websockets_opening_handshake_003_html',
        'websockets/WebPlatformTest.Run/websockets_opening_handshake_005_html',
    ]
    return filters

  # TODO(b/292007482): Replace static list with gn query.
  def GetTestTargets(self):
    return [
        'audio_test',
        'base_unittests',
        'base_test',
        'bindings_test',
        'browser_test',
        'components_metrics_tests',
        'crypto_impl_test',
        'crypto_unittests',
        'csp_test',
        'cssom_test',
        'css_parser_test',
        'cwrappers_test',
        'dom_parser_test',
        'dom_test',
        # TODO(b/292127297): This target is not built for all platforms.
        # 'ffmpeg_demuxer_test',
        'extension_test',
        'graphics_system_test',
        'js_profiler_test',
        'layout_test',
        'layout_tests',
        'loader_test',
        'math_test',
        'media_capture_test',
        'media_session_test',
        'media_stream_test',
        'media_test',
        'memory_store_test',
        'metrics_test',
        'network_test',
        'net_unittests',
        'overlay_info_test',
        'persistent_settings_test',
        'png_utils_test',
        'render_tree_test',
        'renderer_test',
        'scroll_engine_tests',
        'speech_test',
        'storage_test',
        'text_encoding_test',
        'watchdog_test',
        'web_animations_test',
        'webdriver_test',
        'web_test',
        'websocket_test',
        'worker_test',
        'xhr_test',
        'zip_unittests',
    ]

  def GetTestBlackBoxTargets(self):
    return [
        'blackbox',
    ]
