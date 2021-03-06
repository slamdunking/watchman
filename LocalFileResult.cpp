#include "LocalFileResult.h"
#include "ContentHash.h"
#include "watchman_error_category.h"
namespace watchman {

LocalFileResult::LocalFileResult(
    const std::shared_ptr<w_root_t>& root,
    w_string_piece path,
    w_clock_t clock)
    : root_(root), path_(path.asWString()), clock_(clock) {}

void LocalFileResult::getInfo() const {
  if (!needInfo_) {
    return;
  }
  needInfo_ = false;
  try {
    info_ = getFileInformation(path_.c_str(), root_->case_sensitive);
    exists_ = true;
  } catch (const std::exception&) {
    // Treat any error as effectively deleted
    exists_ = false;
  }
}

const watchman::FileInformation& LocalFileResult::stat() const {
  getInfo();
  return info_;
}

w_string_piece LocalFileResult::baseName() const {
  return w_string_piece(path_).baseName();
}

w_string_piece LocalFileResult::dirName() {
  return w_string_piece(path_).dirName();
}

bool LocalFileResult::exists() const {
  getInfo();
  return exists_;
}

watchman::Future<w_string> LocalFileResult::readLink() const {
  auto absPath = w_string::pathCat({root_->root_path, path_});
  return makeFuture(readSymbolicLink(absPath.c_str()));
}

const w_clock_t& LocalFileResult::ctime() const {
  return clock_;
}

const w_clock_t& LocalFileResult::otime() const {
  return clock_;
}

watchman::Future<FileResult::ContentHash> LocalFileResult::getContentSha1() {
  // TODO: find a way to reference a ContentHashCache instance
  // that will work with !InMemoryView based views.
  return makeFuture(makeResultWith([&] {
    auto absPath = w_string::pathCat({root_->root_path, path_});
    return ContentHashCache::computeHashImmediate(absPath.c_str());
  }));
}
} // namespace watchman
